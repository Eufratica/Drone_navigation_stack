# Projeto de Fusão de Sensores com EKF em ROS

**Autor:** Gerson Daniel Santos Marques  
**Instituição:** Universidade Federal da Bahia (UFBA) - Engenharia da Computação  
**Disciplina/Projeto:** Robótica Móvel / Fusão de Sensores  

## 📌 Descrição do Projeto
Este repositório contém a implementação, configuração e validação de Filtros Estendidos de Kalman (EKF) utilizando o pacote `robot_localization` no ROS Noetic. O objetivo é estimar a odometria de um robô móvel (Husky) simulado no Gazebo, fundindo dados de Odometria de Roda e IMU, e comparando os resultados com os dados reais da simulação (Ground Truth).

Foram testados três cenários de filtragem:
1. `/ekf_odom`: Apenas odometria das rodas.
2. `/ekf_odom_imu`: Fusão de odometria das rodas + IMU.
3. `/ekf_all`: Fusão completa.

## ⚙️ Modificações Críticas no EKF (Os arquivos .yaml)
Durante a parametrização dos filtros, um ajuste fundamental foi realizado na matriz de configuração dos sensores para evitar o fenômeno de "Wheel Slippage" (derrapagem das rodas), que degrada a estimativa de rotação (Yaw) do robô.

Nos arquivos de configuração, as matrizes originais causavam uma disputa de confiança entre as rodas e a IMU. Para resolver isso, fizemos a seguinte alteração:

* **Odometria de Roda (`odom0_config`):** Removemos a medição de Yaw (6ª posição) e da velocidade angular de Yaw (12ª posição). O robô passou a confiar nas rodas apenas para deslocamento linear (X, Y, Vx, Vy).
* **IMU (`imu0_config`):** Mantivemos o Yaw e a velocidade angular ativados. O giroscópio, sendo imune à derrapagem, tornou-se a fonte absoluta de verdade para a orientação do robô.

Inicie a Simulação e o Ambiente:

1. roslaunch lar_gazebo lar_husky.launch

Inicie os Filtros de Kalman:

2.roslaunch sensor_fusion_kalman fusion.launch mode:=2

Gravação e Movimentação:

3.rosbag record -O experimento.bag /ekf_odom/odometry/filtered /ekf_odom_imu/odometry/filtered /ekf_all/odometry/filtered /gt/odom




**Exemplo da configuração otimizada:**
```yaml
# Apenas dados lineares das rodas
odom0_config: [true, true, false, false, false, false, 
               true, true, false, false, false, false, 
               false, false, false]

# Confiança total na IMU para rotação
imu0_config: [false, false, false, false, false, true, 
              false, false, false, false, false, true, 
              true, false, false]


