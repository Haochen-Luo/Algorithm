def single_image_learnable_question_joint(
    args: argparse.Namespace,
    eval_model: BaseEvalModel,
    seed: int = 42,
    max_generation_length: int = 5,
    num_beams: int = 3,
    length_penalty: float = -2.0,
    num_shots: int = 2,
    dataset_name: str = "vqav2",
    alpha = 1/255,
    epsilon = 32/255,
    lr = 0.00001,
    frac:float=0.05,
    epochs = 200,
    target = '<|endofchunk|>',
    full_mode:bool = False,
    base_dir = "simq/",
    ques_num = 1,
    datasets = None,
    skip = 0.0,
    
):
    tokenizer = eval_model.tokenizer
    target = target.lower().strip().replace("_", " ")
    target_token_len = len(tokenizer.encode(target))-1
    print("target_token_len is:",target_token_len)
    effective_num_shots = compute_effective_num_shots(num_shots, args.model)
    train_dataset, test_dataset = datasets if datasets is not None else load_train_test_dataset(dataset_name)
    
    test_dataset = prepare_eval_samples(
        test_dataset,
        args.num_samples if args.num_samples > 0 else len(test_dataset),
        seed,
    )
    if frac < 1.0:
        # Use a subset of the test dataset if frac < 1.0
        test_dataset_size = len(test_dataset)
        subset_size = int(frac * test_dataset_size)
        # generate indices use arange
        indices = np.arange(subset_size)
        test_dataset = torch.utils.data.Subset(test_dataset, indices)


    in_context_samples = get_query_set(train_dataset, args.query_set_size, seed)

    # Create a unique directory based on current timestamp to avoid overwriting
    output_dir = f"oneImgMultiQues_{EVAL_FRAC}"
    output_dir = os.path.join(base_dir,output_dir)
    output_dir = find_next_run_dir(output_dir)
    os.makedirs(output_dir, exist_ok=True)
        
    ################ Attack PART ###########################

    VQA_ROOT = "/scratch/local/ssd/haochen/flamingo_ssd/vqav2_data"
    with open(f"{VQA_ROOT}/v2_mscoco_val2014_annotations.json",'r') as f:
        eval_file = json.load(f)
    annos = eval_file["annotations"]
    quesToImg = {i["question_id"]:i["image_id"] for i in annos}    
    if ques_num != 0:   
        img_to_train_ques = get_img_id_train_ques_map(ques_num)
    else:
        img_to_train_ques = {}
    tpoch = tqdm(test_dataset)
    total_success_rate = []
    image_set = set()
    debug_once = True
    for iter in tpoch:
        item = [iter]
        
        print("item is:",item)
        best_attack = None
        best_loss = torch.tensor(1000.0)
        if quesToImg[item[0]["question_id"]] in image_set:
            continue
        else:
            image_set.add(quesToImg[item[0]["question_id"]])      
       
        train_batch_demo_samples = sample_batch_demos_from_query_set(
            in_context_samples, effective_num_shots, len(item)
        )
        test_batch_demo_samples = sample_batch_demos_from_query_set(
            in_context_samples, effective_num_shots, len(item)
        )

        item_images = []
        item_text = []
        # batch_ans = []
       
        img_id = str(quesToImg[item[0]["question_id"]])
        question_pool = train_question()
        total_ques_list  = get_ques(img_to_train_ques,img_id,ques_num,question_pool)
        total_ques_list.insert(0,item[0]["question"])
        if num_shots > 0:
            print("batch_demo_samples is:",train_batch_demo_samples)
            context_images = [x["image"] for x in train_batch_demo_samples[0]]
        else:
            context_images = []
            
        item_images.append(context_images + [item[0]["image"]])

        train_context_text = "".join([
                eval_model.get_vqa_prompt(
                    question=x["question"], answer=x["answers"][0]
                )
                for x in train_batch_demo_samples[0]
        ])
        test_context_text = "".join([
                eval_model.get_vqa_prompt(
                    question=x["question"], answer=x["answers"][0]
                )
                for x in test_batch_demo_samples[0]
        ])

        if num_shots == 0:
            train_context_text = train_context_text.replace("<image>", "")
            test_context_text = test_context_text.replace("<image>", "")
        
        for ques in total_ques_list:
            if target!="no target":
                item_text.append(
                    train_context_text + eval_model.get_vqa_prompt(question=ques)+" "+target)
            else:
                raise ValueError("no target mode is not supported")

        """ start to attack the question"""
        
        labels_list = []
        input_ids_list = []
        context_token_len_list = []
        attention_mask_list = []
        target_encodings = tokenizer.encode(target,return_tensors="pt")
        
        for ques_text in item_text:
            # print("ques_text is:",ques_text)
            input_encodings = tokenizer(
                    ques_text,padding="longest",
                    truncation=True,return_tensors="pt",max_length=2000)
            context_token_len = len(tokenizer.encode(train_context_text))
            context_token_len_list.append(context_token_len)
            input_ids = input_encodings["input_ids"].to(device)
            # print("input_ids is:",input_ids)
            # print("target encoding is", target_encodings)
            attention_mask = input_encodings["attention_mask"].to(device)
            if target!="no target":
                target_id = tokenizer.encode(target)[1:]           
                if full_mode:
                    labels = get_full_target_label(input_ids, target_id)
                else:
                    labels= target_last_label_only(input_ids,target_id)
            else:
                raise ValueError("no target mode is not supported")
            labels_list.append(labels)
            input_ids_list.append(input_ids)
            attention_mask_list.append(attention_mask)
            
        # create a learnable noise tensor
        noise = torch.randn([1,1,3,224,224], requires_grad=True,device = device)
        input_x_original = eval_model._prepare_images_no_normalize(item_images).to(device)     
        inputs_embs_original = eval_model.model.lang_encoder.get_input_embeddings()(input_ids_list[0])
        inputs_embeds = eval_model.model.lang_encoder.get_input_embeddings()(input_ids_list[0]).clone().detach()
        text_perturb = torch.zeros_like(inputs_embs_original,requires_grad=True)
    
        for ep in range(epochs):
            # clone the input_x
            context_token_len = context_token_len_list[0]
            input_x = input_x_original.clone().detach()
            input_x[0,-1] = input_x[0,-1] + noise
            inputs_embeds = inputs_embeds.clone().detach()
            inputs_embeds = inputs_embeds + text_perturb
            labels = labels_list[ep%len(labels_list)]
            input_ids = input_ids_list[ep%len(input_ids_list)]
            attention_mask = attention_mask_list[ep%len(attention_mask_list)]
            
            loss = eval_model.model(  
                inputs_embeds=inputs_embeds,
                lang_x=input_ids,
                vision_x=input_x,                
                attention_mask=attention_mask,
                labels=labels,
            )[0]

            # total_loss.append(float(loss.item()))
            loss.backward()
            tpoch.set_postfix(loss=loss.item(),best_loss=best_loss.item())
            if ep>(epochs//2) :
                if loss<best_loss:
                    best_loss = loss
                    best_attack = noise.clone().detach()
            grad = noise.grad.detach()
            text_grad = text_perturb.grad.detach()
            mask = torch.ones_like(inputs_embs_original)
            mask[:,:context_token_len] = 0
            mask[:,-target_token_len:] = 0
            # update the noise
            if target != "no target":
                d = torch.clamp(noise - alpha * torch.sign(grad), min=-epsilon, max=epsilon)
                if ep%30==0:print(f"lr is {lr} and epsilon is {epsilon}",torch.max( mask*text_grad*lr),torch.min( mask*text_grad*lr))
                d_text = torch.clamp(text_perturb+ mask*text_grad*lr,min = -0.23,max = 0.27)
            else:
                d = torch.clamp(noise + alpha * torch.sign(grad), min=-epsilon, max=epsilon)
                d_text = torch.clamp(text_perturb- mask*text_grad*lr,min = -0.23,max = 0.27)
            noise.data = d
            noise.grad.zero_()
            text_perturb.data = d_text
            text_perturb.grad.zero_()
            # inputs_embeds = inputs_embs_original +  best_text_attack
            # attacked_inputs_embeds = inputs_embeds.clone().detach()
            
            # res = approximate_embeddings(model = eval_model.model.lang_encoder,input_tensor=inputs_embeds,tokenizer=tokenizer)
            # print("approximate result is:",res)
            

                
        ################# evaluation part #######################
        
        attack  = best_attack     
        
        question_list = agnostic_question()
        question_list.insert(0,item[0]["question"])
        success_count = 0        
        target_success_count = 0
        
        eval_batch_size = 8
        import time
        one_eval = time.time()
      
        for batch_ques in more_itertools.chunked(question_list,eval_batch_size):
            
            eval_text = [test_context_text+eval_model.get_vqa_prompt(question=ques, answer=None) for ques in batch_ques]
            if debug_once:
                # print("eval_text is:",eval_text)
                debug_once = False
            
            outputs = eval_model.get_outputs_attack(
                attack = attack,batch_images=item_images*len(batch_ques),
                batch_text=eval_text,max_generation_length=max_generation_length,
                num_beams=num_beams,length_penalty=length_penalty)
            clean_outputs = eval_model.get_outputs(
                                batch_images=item_images*len(batch_ques),
                batch_text=eval_text,max_generation_length=max_generation_length,
                num_beams=num_beams,length_penalty=length_penalty)
            
            
            process_function = (postprocess_ok_vqa_generation if dataset_name == "ok_vqa" else postprocess_vqa_generation)
            print("attacked outputs is:",outputs)
            print("clean outputs is:",clean_outputs)
            new_predictions = list(map(process_function, outputs))
            clean_newpredictions = list(map(process_function, clean_outputs))
            for i in range(len(new_predictions)):
                if new_predictions[i]!=clean_newpredictions[i]:
                    success_count+=1    
                    # print(new_res[i]["answer"],"|",clean_res[i]["answer"])
                    if new_predictions[i].lower() ==target.lower().split("<")[0]:
                        target_success_count+=1 
        print(f"time cost is using {eval_batch_size}:",time.time()-one_eval)   
        print("success_count is:",success_count,"--**target_success_count is**---:",target_success_count,item[0]["question"])
        with open(f"{output_dir}/results.txt",'a') as f:
            f.write(f"success_count is:{success_count},target_success_count is:{target_success_count},question is:{item[0]['question']},best loss: {best_loss.item()}\n")
        total_success_rate.append({"count":success_count,"target_count":target_success_count})
        np.save(f"{output_dir}/attack__{target_success_count}_{quesToImg[item[0]['question_id']]}.npy",best_attack.cpu().numpy())
    mean_success_rate = np.mean([i["count"] for i in total_success_rate])
    mean_target_success_rate = np.mean([i["target_count"] for i in total_success_rate])
    total_success_rate.append({"mean_count":mean_success_rate,"mean_target_count":mean_target_success_rate})
    json.dump(total_success_rate,open(f"{output_dir}/total_success_rate.json",'w'))
