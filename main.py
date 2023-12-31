import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from data_loading.data_loader import createDataLoaders, createDatasets
from train.train_loader import train
from train.test_loader import test
from models.modelFactory import create_model, printTrainableParams
from performance.eval_metrics import evaluate_performance, plot_and_log
from sklearn.model_selection import StratifiedShuffleSplit
from visualization.explainPred import generateHeatMap
from logs.logging import Logger
from utils.config import *
from utils.device import initialize_device
from utils.arguments import parse_arguments
import time

def main():
    start_time = time.time()
    
    args = parse_arguments()
    # Access the parsed arguments
    MODEL = args.model
    DATASET = args.dataset
    PRETRAINED_BOOL = args.pretrained
    NUM_EPOCHS = args.num_epochs
    EARLY_STOPPING_BOOL = args.early_stopping
    DATA_AUGMENT_BOOL = args.data_augment
    print(f"MODEL: {MODEL}\t"
        f"DATASET: {DATASET}\t"
        f"DATA AUGMENT: {DATA_AUGMENT_BOOL}"
    )
    
    # Check if GPU is available
    DEVICE = initialize_device()

    # Create objects
    log_file = Logger(f"./results/{DATASET}_{MODEL}_log.txt")
    
    LR_LIST = [1e-4, 1e-5, 1e-6]
    BATCHSIZE_LIST = [8, 16, 32, 64]
    # BATCHSIZE_LIST = [128, 256]
    best_metric = np.inf
    best_learningrate = 0
    best_batchsize = 0
    temp_dict = {}
    # for LEARNING_RATE in LR_LIST:
    #     for BATCH_SIZE in BATCHSIZE_LIST:
    #         print(LEARNING_RATE)
    #         print(BATCH_SIZE)
    
    model = create_model(model_name=MODEL, num_classes=NUM_CLASSES, input_channels=3, pretrained=PRETRAINED_BOOL)
    
    # Print model architecture
    # print(model)
    # Print trainable parameters
    printTrainableParams(model)
    model = model.to(DEVICE)


    # Non-Kfold Cross Validation
    # train_loader, val_loader, transforms, sample_images, sample_titles = createDataLoaders(batch_size = BATCH_SIZE, dataset = DATASET, data_augment = DATA_AUGMENT_BOOL)
    # train_accuracy_history, train_loss_history, val_accuracy_history, val_loss_history, val_precision_history, val_recall_history, val_preds, val_targets = train(model, train_loader, val_loader, device, criterion, optimizer, epochs = NUM_EPOCHS)
    # historyDict = {
    #     'train_transform': transforms,
    #     'train_accuracy': train_accuracy_history,
    #     'train_loss': train_loss_history,
    #     'val_accuracy': val_accuracy_history,
    #     'val_loss': val_loss_history,
    #     'val_precision': val_precision_history,
    #     'val_recall': val_recall_history
    # }

    # K-fold Cross Validation
    # CBIS-Dataset
    # X, y, transforms = createDatasets(dataset = DATASET, data_augment = DATA_AUGMENT_BOOL)
    # CBIS-New-Dataset (Testing purposes)
    # train_data, val_data = createDatasets(dataset = DATASET, data_augment = DATA_AUGMENT_BOOL, val_ratio = VAL_RATIO)


    # sss = StratifiedShuffleSplit(n_splits = NUM_FOLDS, train_size = TRAIN_RATIO, random_state = SEED)
    # for i, (train_index, val_index) in enumerate(sss.split(X, y), start=1):
    # for i, (train_index, val_index) in enumerate(sss.split(train_data, val_data), start=1):
    

    # reset_weights(model)
    # print(f"--------FOLD {i}--------")
    start_fold_time = time.time()

    train_loader, val_loader, test_loader, train_transform, sample_images, sample_titles, num_examples = createDataLoaders(BATCH_SIZE, DATASET, DATA_AUGMENT_BOOL)
    transforms = train_transform
    train_accuracy_history, train_loss_history, val_accuracy_history, val_loss_history, val_precision_history, val_recall_history, val_preds, val_targets, early_stopped_epoch = train(model, train_loader, val_loader, DEVICE, epochs = NUM_EPOCHS, early_stopping = EARLY_STOPPING_BOOL)


    train_acc, train_loss, val_acc, val_loss, val_precision, val_recall, val_f1 = evaluate_performance(train_accuracy_history, train_loss_history, val_accuracy_history, val_loss_history, val_precision_history, val_recall_history)

    split_train_accuracy_history.append(train_acc)
    split_train_loss_history.append(train_loss)
    split_val_accuracy_history.append(val_acc)
    split_val_loss_history.append(val_loss)
    split_val_precision_history.append(val_precision)
    split_val_recall_history.append(val_recall)
    split_val_f1_history.append(val_f1)

    # print(f"Time taken for fold {i}; lr: {LEARNING_RATE}; batch_size: {BATCH_SIZE}: {time.time() - start_fold_time}")

    roc_auc, pr_auc = plot_and_log(train_accuracy_history, train_loss_history, val_accuracy_history, val_loss_history, early_stopped_epoch, val_preds, val_targets, NUM_EPOCHS, DATASET, MODEL)
    
    historyDict = {
        'folds': 1,
        'train_transform': transforms,
        'train_accuracy': train_acc,
        'train_loss': train_loss,
        'val_accuracy': val_acc,
        'val_loss': val_loss,
        'val_precision': val_precision,
        'val_recall': val_recall,
        'f1_score': val_f1,
        'roc_auc': roc_auc,
        'prroc_auc': pr_auc
    }

    log_file.log(start_fold_time, historyDict)
        
    if val_loss < best_metric:
        best_metric = val_loss
        best_batchsize = BATCH_SIZE
        best_learningrate = LEARNING_RATE

    generateHeatMap(sample_images, sample_titles, model, DEVICE)
    average_train_acc = np.mean(split_train_accuracy_history)
    average_train_loss = np.mean(split_train_loss_history)
    average_val_acc = np.mean(split_val_accuracy_history)
    average_val_loss = np.mean(split_val_loss_history)
    average_precision = np.mean(split_val_precision_history)
    average_recall = np.mean(split_val_recall_history)
    average_f1 = np.mean(split_val_f1_history)

    finalHistoryDict = {
        'folds': None,
        'train_transform': transforms,
        'train_accuracy': average_train_acc,
        'train_loss': average_train_loss,
        'val_accuracy': average_val_acc,
        'val_loss': average_val_loss,
        'val_precision': average_precision,
        'val_recall': average_recall,
        'val_f1': average_f1,
        'roc_auc': roc_auc,
        'prroc_auc': pr_auc
    }

    log_file.log(start_time, finalHistoryDict)
    print(f"\n{finalHistoryDict}")
    print("-"*50)
    print(f"Train Acc: {train_accuracy_history}")
    print(f"Train Loss: {train_loss_history}")
    print(f"Val Acc: {val_accuracy_history}")
    print(f"Val Loss:{val_loss_history}")
    print(f"Val Precision: {val_precision_history}")
    print(f"Val Recall: {val_recall_history}")
       
    # temp_dict[val_loss] = [BATCH_SIZE, LEARNING_RATE]
    # print(f"Best Metric: {temp_dict[(min(temp_dict))]} with {min(temp_dict)} validation loss")
    # # print(f"Best BATCH_SIZE: {best_batchsize} with {best_metric} validation loss")
    # print("-"*50)
    # print(temp_dict)
    # # print("Testing on Unseen Data")
    # test_perf_dict = test(test_loader, model, DEVICE)
    
    

if __name__ == "__main__":
    main()