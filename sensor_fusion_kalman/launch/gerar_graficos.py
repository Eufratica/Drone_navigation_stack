import bagpy
from bagpy import bagreader
import pandas as pd
import matplotlib.pyplot as plt

# Nome do seu arquivo
b = bagreader('experimento_tcc_v1.bag')

# Lista dos tópicos que queremos plotar
topicos = [
    '/ekf_odom/odometry/filtered',
    '/ekf_odom_imu/odometry/filtered',
    '/ekf_all/odometry/filtered',
    '/gt/odom'
]

# Processa e plota
fig, ax = plt.subplots(3, 1, figsize=(10, 15))

for i, filtro in enumerate(['/ekf_odom', '/ekf_odom_imu', '/ekf_all']):
    # Lê os dados do filtro e do ground truth
    df_filtro = pd.read_csv(b.message_by_topic(f'{filtro}/odometry/filtered'))
    df_gt = pd.read_csv(b.message_by_topic('/gt/odom'))
    
    ax[i].plot(df_filtro['pose.pose.position.x'], df_filtro['pose.pose.position.y'], label='Estimativa')
    ax[i].plot(df_gt['pose.pose.position.x'], df_gt['pose.pose.position.y'], label='Ground Truth', linestyle='--')
    ax[i].set_title(f'Comparação: {filtro}')
    ax[i].legend()
    ax[i].grid(True)

plt.tight_layout()
plt.savefig('comparativo_tcc.png')
print("Gráfico 'comparativo_tcc.png' gerado com sucesso!")
