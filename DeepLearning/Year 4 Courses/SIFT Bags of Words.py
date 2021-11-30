# %% Step 2

import time
from collections import Counter, Iterable
import matplotlib.pyplot as plt
import numpy as np
import cv2
import glob
import pickle
from sklearn.cluster import KMeans
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix


def read_images(path=r'D:\COMP338_Assignment1_Dataset\COMP338_Assignment1_Dataset\Training'):
    """
    :param path: image paths
    :return: gray scale images list
    """
    # load if test_dataset_path = r'D:/COMP338_Assignment1_Dataset/COMP338_Assignment1_Dataset/Test/'
    images = []
    dataset_path = path
    images_paths = [image_path for image_path in glob.glob(dataset_path + '//*' + '//*')]
    for img_dir in images_paths:
        img = cv2.imread(str(img_dir), 0)
        images.append(img)
    return images


def load_keypoints(kp_path):
    """

    :param kp_path: file path of stored keypoints
    :return: keypoint list
    """
    # load key points which is obtained from the step1
    kp = []
    with open(kp_path, 'rb') as kp_file:
        raw_kp = pickle.load(kp_file)

    for i in range(len(raw_kp)):
        pic_kp = []
        for point in raw_kp[i]:
            temp = cv2.KeyPoint(x=point[0][0], y=point[0][1], size=point[1], angle=point[2], response=point[3],
                                octave=point[4], class_id=point[5])
            pic_kp.append(temp)
        kp.append(pic_kp)

    return kp


def build_cluster(descriptor, k=(500, 3)):
    """

    :param descriptor: descriptors of training dataset
    :param k: the size of clusters
    :return: single KMeans center or KMeans center list
    """
    if isinstance(k, Iterable):
        cluster_centers = []
        for val in k:
            cluster = KMeans(n_clusters=val, random_state=0).fit(descriptor)
            cluster_centers.append(cluster)
        return cluster_centers
    else:
        cluster = KMeans(n_clusters=k, random_state=0).fit(descriptor)
        return cluster


def load_cluster():
    with open('kmeans20', 'rb') as f:
        kmeans20 = pickle.load(f)
    with open('kmeans500', 'rb') as f2:
        kmeans500 = pickle.load(f2)
    return kmeans500, kmeans20


# %%
# clusters = build_cluster()


# %%  Step 3

def assign_nearest_center(single_desc, vocabulary):
    """
    :param single_desc: single descriptor
    :param vocabulary: 500 or smaller words dictionary
    :return: closest center to the descriptor
    """
    distances = []
    for center in vocabulary:
        distances.append(np.linalg.norm(single_desc - center))
    return np.argmin(distances)


def update_instance_frequency(id, pic_desc, vocabulary, train_frequency):
    """
    :param id: the index of an instance
    :param pic_desc: the total discriptors
    :param vocabulary: codebook vocabulary
    :param train_frequency: the numpy array to be updated
    :return: the features of the images. It is the representation of images
    """
    for i in range(len(pic_desc)):
        closest_idx = assign_nearest_center(pic_desc[i], vocabulary)
        train_frequency[id][closest_idx] += 1
    train_frequency[id] = train_frequency[id] / sum(train_frequency[id])
    return train_frequency


def build_histogram_feature(kp, desc, vocab500, freq_500, vocab20, freq_20, images=None):
    # get the image representation

    for idx, pair in enumerate(zip(kp, desc)):
        pic_kp, pic_desc = pair
        update_instance_frequency(idx, pic_desc, vocab500, freq_500)
        update_instance_frequency(idx, pic_desc, vocab20, freq_20)
    return freq_500, freq_20


# %% Step 4,5,6,7
def intersection(a, b):
    """
    a,b: two L1 normalized histograms
    :return： the negative value of the common area
    """
    common_area = 0
    for i in range(len(a)):
        common_area += min(a[i], b[i])
    return -common_area


def evaluate_model(model_type, train_X, train_y, test_X, test_y):
    """

    :param model_type: two types model available, the metrics are euclidean and intersection respectively
    :param train_X: training features of images
    :param train_y: training labels
    :param test_X: training features of images
    :param test_y: testing labels
    :return:
    """
    if model_type.split(' ')[0] == 'eu':
        metric = 'minkowski'
    else:
        metric = intersection
    model = KNeighborsClassifier(n_neighbors=1, metric=metric)
    model.fit(train_X, train_y)
    predictions = model.predict(test_X)
    acc = model.score(test_X, test_y)
    confusion_mat = confusion_matrix(test_y, predictions)
    report = classification_report(test_labels, model.predict(test_X))
    print(acc, '\n', confusion_mat, '\n', report)
    print('end of the evaluation of %s\n' % model_type)
    return model, predictions, acc, confusion_mat, report


def save_model(model_name, model):
    with open(model_name, 'wb') as m:
        pickle.dump(model, m)


def same_codeword_visualization(images, keypoints, desc, vocab, codeword_idx=295, start=0):
    """

    :param images: training images of testing images list
    :param keypoints: key points of the training or testing images
    :param desc: descriptors of training or testing data
    :param vocab: vocabulary of codebook
    :param codeword_idx: the cluster center
    :param start: start of the visualization index
    """
    plt.figure()
    row = 2
    col = 5
    for demo_id in range(start, start + 10):
        demo_img = images[demo_id]
        offset = start - 1
        plt.subplot(row, col, demo_id - offset)
        kp = keypoints[demo_id]
        dp = desc[demo_id]
        for k, p in zip(kp, dp):
            if assign_nearest_center(p, vocab) == codeword_idx:
                demo_img = cv2.drawKeypoints(demo_img, [k], demo_img)
        plt.imshow(demo_img)
        plt.title(demo_id)
    plt.show()


def display_pic(images, pic_idx):
    """
    display images according to the given picture indices
    :param images: training images or testing images
    :param pic_idx: picture indices
    """
    plt.figure(5)
    for id, demo_id in enumerate(pic_idx):
        plt.subplot(1, 5, id + 1)
        demo_img = images[demo_id]
        plt.imshow(demo_img, cmap='gray')
        plt.show()


def classify_result(y_pred, y_true):
    """

    :param y_pred: model predition
    :param y_true: ground truth label
    :return: indices of correct and wrong numbers
    """
    mis_classified = []
    correct = []
    for i in range(len(y_pred)):
        if y_true[i] != y_pred[i]:
            mis_classified.append(i)
        else:
            correct.append(i)
    return correct, mis_classified


def find_class(index):
    # bound is a cumulative sum  the number of descriptors of each image
    bound = [95, 416, 586, 1036, 1347, 1906, 2399, 2567, 2831, 2937, 3280, 3433, 3928, 4229, 4571, 5011, 5268, 5684,
             6152, 6614,
             6728, 6949, 7077, 7491, 7891, 8082, 8252, 8707, 8881, 9102, 9700, 9951, 10084, 10321, 10789, 11220, 11590,
             12034, 12135, 12418,
             13025, 13420, 13833, 14226, 14350, 14772, 15067, 15585, 15984, 16187, 16706, 17007, 17346, 17474, 17759,
             17943, 18410, 18864, 19088, 19351,
             19549, 20033, 20301, 20599, 20733, 20864, 21149, 21522, 21626, 22075, 22408, 22734, 23089, 23442, 23779,
             24100, 24600, 25057, 25465, 25741,
             25991, 26412, 26916, 27260, 27646, 28184, 28628, 29056, 29607, 30073, 30550, 31093, 31567, 31894, 32229,
             32470, 32851, 33199, 33629, 34015,
             34276, 34729, 35169, 35592, 36081, 36484, 37044, 37503, 37929, 38321, 38777, 39110, 39639, 40128, 40553,
             41064, 41532, 42008, 42572, 43071,
             43534, 43978, 44524, 45049, 45567, 46127, 46797, 47319, 47866, 48400, 48932, 49239, 49676, 50203, 50642,
             51083, 51401, 51645, 51896, 52083,
             52359, 52840, 53185, 53485, 53909, 54530, 54841, 55575, 56036, 56665, 57005, 57255, 57717, 58018, 58419,
             59015, 59310, 59639, 60407, 60752,
             61212, 61598, 61967, 62441, 62718, 63088, 63554, 63718, 64096, 64648, 65068, 65377, 65888, 66182, 66558,
             67524, 67856, 68586, 68852, 69162,
             69524, 69845, 70434, 70662, 70987, 71054, 71793, 71991, 72365, 72745, 73484, 74114, 74875, 75223, 75442,
             75840, 76278, 76521, 76793, 77254,
             77456, 78232, 78841, 79020, 79439, 80142, 80513, 81004, 81189, 81545, 81895, 82332, 82611, 82850, 83301,
             83636, 83798, 83928, 84098, 84228,
             84454, 84597, 84989, 85169, 85302, 85563, 86006, 86387, 86726, 87279, 87548, 87748, 87962, 88302, 88682,
             89014, 89288, 89445, 89669, 90011,
             90410, 90799, 91105, 91492, 91893, 92198, 92387, 92773, 92896, 93099, 93267, 93526, 93873, 94255, 94547,
             94901, 95097, 95244, 95593, 95931,
             96164, 96579, 96910, 97236, 97463, 97690, 97799, 98082, 98231, 98411, 98668, 99003, 99244, 99520, 99708,
             100269, 100551, 100763, 101080, 101401,
             101529, 101983, 102261, 102539, 102919, 103455, 104037, 104660, 105022, 105582, 106072, 106618, 106972,
             107296, 107416, 107814, 108126, 108730, 109058, 109477,
             109893, 110537, 110965, 111431, 111888, 112270, 112635, 113161, 113732, 114078, 114360, 114567, 114831,
             115315, 115711, 116249, 116722, 117019, 117285, 117718,
             118073, 118329, 118884, 119211, 119361, 119529, 120314, 120642, 121008, 121208, 121470, 121840, 122100,
             122580, 123138, 123875, 124309, 125102, 125579, 126162,
             126477, 126844, 127571, 127982, 128351, 129364, 129678, 130382, 130587, 131053]
    for i in range(len(bound)):
        if index < bound[i]:
            print('belongs to class', i // 70)
            return i // 70


def get_desc_class_distribution(centers, descriptors):
    """

    :param centers: the cluster centers
    :param descriptors: descriptors of pictures
    :return: the distribution of descriptors of each cluster center
    """
    class_distribute = []
    stacked = np.vstack(descriptors)
    for i in range(len(centers)):
        # print((centers[i]-stacked).shape)
        index = np.argmin(np.linalg.norm(centers[i] - stacked, axis=1))
        class_distribute.append(find_class(index))
    res = Counter(class_distribute)
    # print(res)
    return res


# %%

if __name__ == '__main__':
    # %%
    save_mode = False  # save model or not

    # Specify the path of key points and descriptors to load
    train_kp_path = r'train_keypoints.pickle'
    train_desc_path = r'train_descriptors.npy'
    test_kp_path = r'test_keypoints.pickle'
    test_desc_path = r'test_descriptors.npy'
    train_image_path = r'D:\COMP338_Assignment1_Dataset\COMP338_Assignment1_Dataset\Training'
    test_image_path = r'D:\COMP338_Assignment1_Dataset\COMP338_Assignment1_Dataset\Test'

    # load the key points and descriptors
    train_kp = load_keypoints(train_kp_path)
    train_desc = np.load(train_desc_path, allow_pickle=True)
    test_kp = load_keypoints(test_kp_path)
    test_desc = np.load(test_desc_path, allow_pickle=True)
    train_images = read_images(train_image_path)
    test_images = read_images(test_image_path)

    # Specify the number of the training and testing instance
    TRAIN_NUM = 350
    TEST_NUM = 50

    # Generate the labels for the training and testing data
    train_labels = [0] * 70 + [1] * 70 + [2] * 70 + [3] * 70 + [4] * 70
    test_labels = [0] * 10 + [1] * 10 + [2] * 10 + [3] * 10 + [4] * 10

    # step 3
    train_freq_500 = np.zeros((TRAIN_NUM, 500))
    train_freq_20 = np.zeros((TRAIN_NUM, 20))
    test_freq_500 = np.zeros((TEST_NUM, 500))
    test_freq_20 = np.zeros((TEST_NUM, 20))

    clusters = load_cluster()  # you may also choose build_cluster() to build clusters from scratch
    vocab500 = clusters[0].cluster_centers_
    vocab20 = clusters[1].cluster_centers_

    start_time = time.time()
    build_histogram_feature(train_kp, train_desc, vocab500, train_freq_500, vocab20, train_freq_20)
    t2 = time.time() - start_time
    print(train_freq_20, train_freq_500)
    print('built takes %f seconds' % (t2))
    build_histogram_feature(test_kp, test_desc, vocab500, test_freq_500, vocab20, test_freq_20)
    print(test_freq_20, test_freq_500)
    t3 = time.time() - t2
    print('built takes %f seconds' % (t3))

    if save_mode:
        np.save('train_frequency_20.npy', train_freq_20)
        np.save('train_frequency_500.npy', train_freq_500)
        np.save('test_frequency_20.npy', test_freq_20)
        np.save('test_frequency_500.npy', test_freq_500)

    # Step 4,5,6
    # Evaluate the model with the (vocabulary = 20 or 500) * (distance  = 'euclidean' or 'frequency')
    eu_20_result = evaluate_model('eu 20', train_freq_20, train_labels, test_freq_20, test_labels)
    fr_20_result = evaluate_model('fr 20', train_freq_20, train_labels, test_freq_20, test_labels)
    eu_500_result = evaluate_model('eu 500', train_freq_500, train_labels, test_freq_500, test_labels)
    fr_500_result = evaluate_model('fr 500', train_freq_500, train_labels, test_freq_500, test_labels)

    if save_mode:
        save_model('eu_500_model', eu_500_result[0])
        save_model('eu_20_model', eu_20_result[0])
        save_model('fr_500_model', fr_500_result[0])
        save_model('fr_20_model', fr_20_result[0])

    # Visualization parts of this coursework

    # Visualize the patches belong to the same codeword
    same_codeword_visualization(train_images, train_kp, train_desc, vocab500, codeword_idx=295)

    # display the images that are misclassified
    mis, correct = classify_result(eu_500_result[1], test_labels)
    print(mis)
    print(correct)
    correct, mis_classified = classify_result(eu_500_result[1], test_labels)
    # print(correct)
    # print(mis_classified)

    display_pic(test_images, [0, 17, 21, 32, 40])
    display_pic(test_images, [1, 11, 22, 33, 42])

    # Step 7: Explain the cause of the failure
    class_dis_500 = get_desc_class_distribution(vocab500, train_desc)
    class_dis_20 = get_desc_class_distribution(vocab20, train_desc)

    # additional experiments

    avg_feature500 = []
    for i in range(5):
        avg_feature500.append(np.mean(train_freq_500[i * 70:(i + 1) * 70], axis=0))
        # print(np.mean(train_freq_500[i*70:(i+1)*70]).shape)

    avg_feature = np.array(avg_feature500)
    evaluate_model('fr 500avg', avg_feature, [0, 1, 2, 3, 4], test_freq_500, test_labels)
    evaluate_model('eu 500avg', avg_feature, [0, 1, 2, 3, 4], test_freq_500, test_labels)
    # additional experient
    avg_feature20 = []

    for i in range(5):
        avg_feature20.append(np.mean(train_freq_20[i * 70:(i + 1) * 70], axis=0))
        # print(np.mean(train_freq_500[i*70:(i+1)*70]).shape)
    avg_feature = np.array(avg_feature20)
    evaluate_model('fr 20avg', avg_feature20, [0, 1, 2, 3, 4], test_freq_20, test_labels)
    evaluate_model('eu 20avg', avg_feature20, [0, 1, 2, 3, 4], test_freq_20, test_labels)

    # additional experiments

    avg_feature500 = []
    for i in range(5):
        avg_feature500.append(np.mean(train_freq_500[i * 70:(i + 1) * 70], axis=0))
        # print(np.mean(train_freq_500[i*70:(i+1)*70]).shape)

    avg_feature = np.array(avg_feature500)
    evaluate_model('fr 500avg', avg_feature, [0, 1, 2, 3, 4], test_freq_500, test_labels)
    evaluate_model('eu 500avg', avg_feature, [0, 1, 2, 3, 4], test_freq_500, test_labels)
    # additional experiment
    avg_feature20 = []

    for i in range(5):
        avg_feature20.append(np.mean(train_freq_20[i * 70:(i + 1) * 70], axis=0))
        # print(np.mean(train_freq_500[i*70:(i+1)*70]).shape)
    avg_feature = np.array(avg_feature20)
    evaluate_model('fr 20avg', avg_feature20, [0, 1, 2, 3, 4], test_freq_20, test_labels)
    evaluate_model('eu 20avg', avg_feature20,[0,1,2,3,4], test_freq_20, test_labels)
