#!/usr/bin/env python3
import rosbag
import numpy as np
import matplotlib.pyplot as plt
import os

# Tópicos padrão gerados pelo fusion.launch e Gazebo
TOPIC_GT = '/gt/odom'
TOPIC_EST = '/odometry/filtered_tcc'

def extrair_dados(bag_file, topico):
    t_list, x_list, y_list = [], [], []
    if not os.path.exists(bag_file):
        return [], [], []
        
    with rosbag.Bag(bag_file, 'r') as bag:
        for topic, msg, t in bag.read_messages(topics=[topico]):
            t_list.append(t.to_sec())
            x_list.append(msg.pose.pose.position.x)
            y_list.append(msg.pose.pose.position.y)
    return t_list, x_list, y_list

def processar_e_plotar(bag_file, titulo, nome_saida):
    if not os.path.exists(bag_file):
        print(f"[AVISO] Arquivo {bag_file} não encontrado. Grave-o para gerar este gráfico.")
        return

    print(f"Processando: {bag_file}...")
    
    t_gt, x_gt, y_gt = extrair_dados(bag_file, TOPIC_GT)
    t_est, x_est, y_est = extrair_dados(bag_file, TOPIC_EST)
    
    if len(t_gt) == 0 or len(t_est) == 0:
        print(f"[AVISO] Faltando dados no {bag_file}. Verifique se os tópicos foram gravados corretamente.\n")
        return

    # Alinhamento de Origem (Elimina o Offset)
    x_gt_al = np.array(x_gt) - x_gt[0]
    y_gt_al = np.array(y_gt) - y_gt[0]
    x_est_al = np.array(x_est) - x_est[0]
    y_est_al = np.array(y_est) - y_est[0]

    # Interpolação para cálculo de erro
    x_est_interp = np.interp(t_gt, t_est, x_est_al)
    y_est_interp = np.interp(t_gt, t_est, y_est_al)

    # Cálculo do RMSE
    erro_quadratico = (x_est_interp - x_gt_al)**2 + (y_est_interp - y_gt_al)**2
    rmse = np.sqrt(np.mean(erro_quadratico))

    print(f"--- {titulo} ---")
    print(f"RMSE: {rmse:.4f} m\n")

    # Plotagem
    plt.figure(figsize=(10, 6))
    plt.plot(x_gt_al, y_gt_al, label='Ground Truth (Real)', linestyle='--', color='darkorange', linewidth=2)
    plt.plot(x_est_al, y_est_al, label='Estimativa EKF', color='royalblue', linewidth=2)

    plt.title(f'{titulo} | RMSE: {rmse:.4f} m', fontsize=14, fontweight='bold')
    plt.xlabel('Posição X (metros)', fontsize=12)
    plt.ylabel('Posição Y (metros)', fontsize=12)
    plt.legend(loc='best')
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.axis('equal') 

    plt.savefig(nome_saida, dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == '__main__':
    processar_e_plotar('mode1.bag', 'Mode 1: Odometria Pura', 'resultado_mode1_odom.png')
    processar_e_plotar('mode2.bag', 'Mode 2: Odometria + IMU', 'resultado_mode2_odom_imu.png')
    processar_e_plotar('mode3.bag', 'Mode 3: Odom + IMU + GPS', 'resultado_mode3_odom_imu_gps.png')
    
    print("[OK] Script finalizado!")
