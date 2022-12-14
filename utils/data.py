import glob 
import pandas as pd
from tensorflow.keras.preprocessing.image import ImageDataGenerator

data_training = pd.DataFrame()
image_path = glob.glob('/TrainDataset/images/training/*')
image_path.sort()
mask_path = glob.glob('/TrainDataset/annotations/training/*')
mask_path.sort()
data_training['image_path'] = image_path
data_training['mask_path'] = mask_path

data_validation = pd.DataFrame()
image_path = glob.glob('/TrainDataset/images/validation/*')
image_path.sort()
mask_path = glob.glob('/TrainDataset/annotations/validation/*')
mask_path.sort()
data_validation['image_path'] = image_path
data_validation['mask_path'] = mask_path

data_test = pd.DataFrame()
image_path = glob.glob('/TestDataset/Kvasir/images/*')
image_path.sort()
mask_path = glob.glob('/TestDataset/Kvasir/masks/*')
mask_path.sort()
data_test['image_path'] = image_path
data_test['mask_path'] = mask_path


def train_generator(data_frame, batch_size, aug_dict,
        image_color_mode="rgb",
        mask_color_mode="grayscale",
        image_save_prefix="image",
        mask_save_prefix="mask",
        save_to_dir=None,
        target_size=(256,256),
        seed=1):

    image_datagen = ImageDataGenerator(**aug_dict)
    mask_datagen = ImageDataGenerator(**aug_dict)
    
    image_generator = image_datagen.flow_from_dataframe(
        data_frame,
        x_col = "image_path",
        class_mode = None,
        color_mode = image_color_mode,
        target_size = target_size,
        batch_size = batch_size,
        save_to_dir = save_to_dir,
        save_prefix  = image_save_prefix,
        seed = seed)

    mask_generator = mask_datagen.flow_from_dataframe(
        data_frame,
        x_col = "mask_path",
        class_mode = None,
        color_mode = mask_color_mode,
        target_size = target_size,
        batch_size = batch_size,
        save_to_dir = save_to_dir,
        save_prefix  = mask_save_prefix,
        seed = seed)

    train_gen = zip(image_generator, mask_generator)
    
    for (img, mask) in train_gen:
        img, mask = adjust_data(img, mask)
        yield (img,mask)

def adjust_data(img,mask):
    img = img / 255.
    mask = mask / 255.
    mask[mask > 0.5] = 1
    mask[mask <= 0.5] = 0
    
    return (img, mask)

