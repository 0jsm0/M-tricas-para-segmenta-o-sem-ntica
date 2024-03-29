#metricas
import cv2
import os
import numpy as np
import glob

def calculate_metrics(gt_path, pred_path):
    # Listas para armazenar os IoUs e Dice calculados de cada imagem
    iou_scores = []
    dice_scores = []

    # Obter lista de arquivos nos diretórios
    gt_files = glob.glob(os.path.join(gt_path, "*.png"))
    pred_files = glob.glob(os.path.join(pred_path, "*.png"))

    # Garantir que temos a mesma quantidade de arquivos em ambas as pastas
    assert len(gt_files) == len(pred_files)

    # Iterar sobre os arquivos
    for gt_file, pred_file in zip(gt_files, pred_files):
        # Ler imagens de gt e pred
        gt_image = cv2.imread(gt_file, cv2.IMREAD_GRAYSCALE)
        pred_image = cv2.imread(pred_file, cv2.IMREAD_GRAYSCALE)

        # Redimensionar pred para 1280x1918 se necessário
        if pred_image.shape[:2] != (1918, 1280):
            pred_image = cv2.resize(pred_image, (1918, 1280))

        # Binarizar gt e pred
        _, gt_image = cv2.threshold(gt_image, 127, 255, cv2.THRESH_BINARY)
        _, pred_image = cv2.threshold(pred_image, 127, 255, cv2.THRESH_BINARY)

        # Calcular IoU
        intersection = np.logical_and(gt_image, pred_image)
        union = np.logical_or(gt_image, pred_image)
        iou_score = np.sum(intersection) / np.sum(union)
        iou_scores.append(iou_score)

        # Calcular Dice
        dice_score = 2 * np.sum(intersection) / (np.sum(gt_image) + np.sum(pred_image))
        dice_scores.append(dice_score)

        # Exibir o IoU e o Dice de cada imagem individualmente
        print(f"IoU da imagem {os.path.basename(gt_file)}: {iou_score}")
        print(f"Dice da imagem {os.path.basename(gt_file)}: {dice_score}")

    # Calcular a média dos IoUs e Dices
    mean_iou = np.mean(iou_scores)
    mean_dice = np.mean(dice_scores)

    # Exibir a média dos IoUs e Dices
    print(f"Média do IoU: {mean_iou}")
    print(f"Média do Dice: {mean_dice}")

# Exemplo de uso da função
gt_path = r"C:\Users\julio\segmentacao\masks_png"
pred_path = r"C:\Users\julio\segmentacao\saved_images"
calculate_metrics(gt_path, pred_path)
