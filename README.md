# Drone Navigation Stack - UFBA

Este repositório contém a stack de navegação autônoma para veículos aéreos não tripulados (UAVs) integrados ao ecossistema ArduPilot/SITL via MAVROS. O foco principal é a integração entre o planejamento de caminho (`move_base`) e o controle de voo (`ArduCopter`).



## Arquitetura do Sistema

O sistema funciona através de uma ponte entre o alto nível (ROS) e o baixo nível (Firmware):

* **SITL (Software In The Loop):** Simulação física do ArduPilot.
* **MAVROS:** Tradutor de mensagens MAVLink para tópicos ROS.
* **MoveBase:** Planejador global e local.
* **Script de Conversão:** Tradutor de mensagens `Twist` para `TwistStamped`.

## Adaptações e Resolução de Problemas

### 1. Resolução do Mismatch de Tipos (Datatype)
O `move_base` publica mensagens do tipo `geometry_msgs/Twist`, mas o MAVROS exige `geometry_msgs/TwistStamped`.
* **Solução:** Implementamos o script `cmd_vel_to_stamped.py` que subscreve o tópico `/cmd_vel_raw`, injeta o `header` de tempo atual e republica no `/mavros/setpoint_velocity/cmd_vel`.

### 2. Problemas de TF (Árvores Desconectadas)
Durante o desenvolvimento, o RViz apresentava erros constantes de `unconnected trees` (não conexão entre `map`, `odom` e `base_link`).
* **Adaptação:** * Otimizamos a árvore de transformações para navegar em referência ao frame `odom`.
    * Utilizamos `static_transform_publisher` para conectar o Laser (`hokuyo_sensor_link`) ao chassis (`base_link`) e o `odom` ao `base_link`.
    * Removemos dependências desnecessárias de pacotes de terceiros (como `mocap_pose_tf`) que causavam falhas de runtime.

### 3. Comportamento de Oscilação/Giro
Observou-se que, após o envio de um novo *2D Nav Goal*, o drone por vezes apresentava movimentos de rotação indevidos ("giro no mesmo local").
* **Causa:** Conflito entre a odometria calculada pelo ROS e a posição absoluta reportada pelo MAVROS, além de tolerâncias muito restritas.
* **Ajuste:** Alteramos os parâmetros em `base_local_planner_params.yaml` para aumentar as tolerâncias (`yaw_goal_tolerance` e `xy_goal_tolerance`) e garantir que o `move_base` entenda quando o objetivo foi atingido, evitando o loop de correção.

## Como Rodar

### Pré-requisitos
* ROS (Noetic ou similar)
* MAVROS instalado e configurado
* Gazebo e ArduPilot SITL

### Execução
1. **Terminal 1:** `sim_vehicle.py -v ArduCopter -f gazebo-iris`
2. **Terminal 2:** `roslaunch mavros apm.launch`
3. **Terminal 3:** `roslaunch drone_navigation navigation.launch`
4. **Terminal 4:** `rviz -d seu_setup_drone.rviz`

> **Nota:** Para decolagem, utilize o console do MAVProxy: `arm throttle`, `mode GUIDED`, `takeoff 3`.

## Dicas Adicionais

* **Navegação:** O sistema está configurado para operar com o `global_frame` em `odom`. Isso garante estabilidade em ambientes fechados onde o GPS pode sofrer interferência.
* **Controle:** Se o drone for agressivo, ajuste os valores de `max_vel_x` e `max_rot_vel` no arquivo `base_local_planner_params.yaml`.

---

**Autor:** Gerson Daniel Santos Marques  
**Projeto:** Engenharia de Computação - UFBA
