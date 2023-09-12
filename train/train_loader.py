import torch 
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.model_selection import cross_validate
from visualization.explainPred import generateHeatMap
import time

def train(model, train_loader, val_loader, device, criterion, optimizer, epochs):
    train_loss_history = []
    train_accuracy_history = []
    val_loss_history = []
    val_accuracy_history = []
    val_precision_history = []
    val_recall_history = []
    print("Starting training now")
    for epoch in range(epochs):
        start_train_time = time.time()
        model.train()
        train_loss = 0.0
        correct_train = 0
        total_train = 0
        for batch_num, (inputs, labels) in enumerate(train_loader):
            # print("In Train_loader")
            # print(f"Current Batch: {batch_num}")
            # print(inputs, labels)
            # print(type(inputs), type(labels))
            model.to(device)
            labels = labels.type(torch.LongTensor)
            inputs, labels = inputs.to(device), labels.to(device)

            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            train_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            total_train += labels.size(0)
            correct_train += (predicted == labels).sum().item()
            batch_num += 1
        
        train_accuracy = correct_train / total_train
        train_loss_history.append(train_loss / len(train_loader))
        train_accuracy_history.append(train_accuracy)
        
        print(f"Train time: {(time.time() - start_train_time):.2f}s")
        
        
        
        # Validation
        start_val_time = time.time()
        print("Starting Validation")
        model.eval()
        val_loss = 0.0
        correct_val = 0
        total_val = 0
        val_preds = []
        val_targets = []
        
        with torch.no_grad():
            for inputs, labels in val_loader:
                model.to(device)
                labels = labels.type(torch.LongTensor)
                inputs, labels = inputs.to(device), labels.to(device)
                outputs = model(inputs)
                loss = criterion(outputs, labels)
                
                val_loss += loss.item()
                _, predicted = torch.max(outputs.data, 1)
                total_val += labels.size(0)
                correct_val += (predicted == labels).sum().item()
                val_preds.extend(predicted.cpu().numpy())
                val_targets.extend(labels.cpu().numpy())
            
        val_accuracy_history.append(correct_val / total_val)
        val_loss_history.append(val_loss / len(val_loader))
        val_accuracy_score = accuracy_score(val_targets, val_preds)
        val_precision = precision_score(val_targets, val_preds, average='weighted')
        val_precision_history.append(val_precision)
        val_recall = recall_score(val_targets, val_preds, average='weighted')
        val_recall_history.append(val_recall)
        val_f1 = f1_score(val_targets, val_preds, average='weighted')
        val_confusion = confusion_matrix(val_targets, val_preds)
    
        
        print(f"Val time: {(time.time() - start_val_time):.2f}s")
        print(f"Epoch [{epoch+1}/{epochs}] - "
            f"Train Loss: {train_loss_history[-1]:.4f}, Train Accuracy: {train_accuracy:.4f} - "
            f"\nValidation Loss: {val_loss_history[-1]:.4f}, "
            f"Validation Accuracy: {val_accuracy_score:.4f}")
            # f"Validation Precision: {val_precision:.4f}, "
            # f"Validation Recall: {val_recall:.4f}, "
            # f"Validation F1-score: {val_f1:.4f}")

    # generateHeatMap(val_loader, model, device)
    
    

    return train_accuracy_history, train_loss_history, val_accuracy_history, val_loss_history, val_precision_history, val_recall_history, val_preds, val_targets