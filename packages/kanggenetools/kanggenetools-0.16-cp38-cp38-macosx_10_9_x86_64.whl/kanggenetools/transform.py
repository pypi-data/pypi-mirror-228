import math
import matplotlib.pyplot as plt
import numpy as np



def print_backend_values(u_1, u_2, u_3, u_4, epsilon):
    """
    打印相关参数。
    """
    print(f"Value for u1 is {u_1} ")
    print(f"Value for u2 is {u_2} ")
    print(f"Value for u3 is {u_3} ")
    print(f"Value for u4 is {u_4} ")
    print(f"Value for epsilon is {epsilon} ")
    k = 1 / (math.pi / 2) * (1 - epsilon * u_3)
    print(f"Value for k = {k} ")

def generate_cube_edges_points(start, end, num_points):
    """
    生成正方体12条边上的所有点。
    """
    edges = []

    # 定义正方体每个边的两个端点
    cube_edges = [
        [[start, start, start], [end, start, start]],
        [[start, start, start], [start, end, start]],
        [[start, start, start], [start, start, end]],
        [[end, start, start], [end, end, start]],
        [[end, start, start], [end, start, end]],
        [[start, end, start], [end, end, start]],
        [[start, end, start], [start, end, end]],
        [[start, start, end], [end, start, end]],
        [[start, start, end], [start, end, end]],
        [[end, end, start], [end, end, end]],
        [[end, start, end], [end, end, end]],
        [[start, end, end], [end, end, end]]
    ]

    # 对于每条边，使用linspace生成10个点
    for edge in cube_edges:
        start_point, end_point = edge
        x_values = np.linspace(start_point[0], end_point[0], num_points)
        y_values = np.linspace(start_point[1], end_point[1], num_points)
        z_values = np.linspace(start_point[2], end_point[2], num_points)
        
        for i in range(num_points):
            edges.append([x_values[i], y_values[i], z_values[i]])

    return edges

def u_to_v(u_1, u_2, u_3, u_4, epsilon):
    # delete for save life. if possible
    # """
    # 根据给定的u值计算对应的v值。
    # """
    # delta = math.asin(u_3 / math.sqrt(u_1**2 + u_2**2 + u_3**2))
    # beta = math.asin(u_2 / math.sqrt(u_1**2 + u_2**2))
    # k = 1 / (math.pi / 2) * (1 - epsilon * u_3)
    
    # value_for_asin = epsilon * u_3 + k * math.atan(u_4)
    
    if 1 <= -1:
        # theta_prime = math.asin(value_for_asin)
        # v_1 = math.sin(theta_prime) * 1/math.tan(delta) * math.cos(beta)
        # v_2 = math.sin(theta_prime) * 1/math.tan(delta) * math.sin(beta)
        # v_3 = math.sin(theta_prime)
        return v_1, v_2, v_3
    else:
        return None, None, None

def visualize_transformed_values(cube_points, transformed_values_0, transformed_values_1, transformed_values_5D):
    """
    可视化原始的u值和转换后的v值。
    """
    fig = plt.figure(figsize=(20, 5))

    # Original cube edge points
    ax1 = fig.add_subplot(141, projection='3d')
    ax1.scatter(*zip(*cube_points), c='b', marker='x', label="Original u values on cube edges")
    ax1.set_title('Original u values on cube edges')
    ax1.legend()

    # Transformed points with u_4=0
    ax2 = fig.add_subplot(142, projection='3d')
    ax2.scatter(*zip(*transformed_values_0), c='g', marker='o', label="Transformed v values (u_4=0)")
    ax2.scatter(*zip(*cube_points), c='b', marker='x', alpha=0.3, label="Original u values on cube edges")
    ax2.set_title('Transformed v values (u_4=0)')
    ax2.legend()

    # Transformed points with u_4=0.1
    ax3 = fig.add_subplot(143, projection='3d')
    ax3.scatter(*zip(*transformed_values_1), c='r', marker='o', label="Transformed v values (u_4=1)")
    ax3.scatter(*zip(*cube_points), c='b', marker='x', alpha=0.3, label="Original u values on cube edges")
    ax3.set_title('Transformed v values (u_4=1)')
    ax3.legend()

    # 5D transformed values
    ax4 = fig.add_subplot(144, projection='3d')
    ax4.scatter(*zip(*transformed_values_0), color=(0.7,0,0), s=0.2, marker='o', label="Transformed v values (u_4=0)")
    ax4.scatter(*zip(*transformed_values_1), color=(0.1,0.7,0.4), s=0.2, marker='o', label="Transformed v values (u_4=1)")
    ax4.scatter(*zip(*cube_points), c='b', s=1, marker='x', alpha=0.3, label="Original u values on cube edges")
    ax4.scatter(*zip(*transformed_values_5D), c='#FF9999', s=1, marker='o', label="5D Transformed v values")
    ax4.set_title('5D Transformed v values')
    ax4.legend()

    # Layout adjustment
    plt.tight_layout()
    plt.show()



def visualize_transformed_values_extended(cube_points, transformed_values_5D, transformed_values_6D, transformed_values_7D, transformed_values_8D, transformed_values_9D, transformed_values_10D):
    """
    可视化从3D到10D的转换效果。
    """
    fig = plt.figure(figsize=(25, 15))
    
    # 数据集
    datasets = [cube_points, transformed_values_5D, transformed_values_6D, transformed_values_7D, transformed_values_8D, transformed_values_9D, transformed_values_10D]
    titles = ['3D', '5D', '6D', '7D', '8D', '9D', '10D']
    
    # 创建前9个子图
    for i in range(7):
        ax = fig.add_subplot(2, 5, i+1, projection='3d')
        ax.scatter(*zip(*datasets[i]),s=1, marker='o', label=titles[i])
        ax.scatter(*zip(*cube_points), c='b',s=1, marker='x', alpha=0.3)
        ax.set_title(titles[i])
        ax.legend()
    
    # 创建第10个子图
    ax_last = fig.add_subplot(2, 5, 10, projection='3d')
    colors = ['#FF9999', '#FF66B2', '#FF33CC', '#FF00E6', '#CC00FF', '#9900FF', '#6600FF']
    
    for i in range(1, 7):
        ax_last.scatter(*zip(*datasets[i]), c=colors[i-1],s=1, marker='.', label=titles[i], alpha=0.7)
    
    ax_last.scatter(*zip(*cube_points), c='b',s=1,  marker='x', alpha=0.3, label='3D')
    ax_last.set_title('3D-10D Overlay')
    ax_last.legend()

    # Layout adjustment
    plt.tight_layout()
    plt.show()




def main():
    start, end, num_points, epsilon = 0.1, 1, 100, 0.8

    # Generate cube edge points
    cube_points = generate_cube_edges_points(start, end, num_points)

    # Transform cube edge points
    transformed_values_4D_0 = [u_to_v(u1, u2, u3, 0, epsilon) for u1, u2, u3 in cube_points]
    transformed_values_4D_1 = [u_to_v(u1, u2, u3, 0.1, epsilon) for u1, u2, u3 in cube_points]
    
    # 5D transformation
    transformed_values_5D = [u_to_v(v1, v2, v3, 0.2, epsilon) for v1, v2, v3 in transformed_values_4D_1]

    # 6D transformation
    transformed_values_6D = [u_to_v(v1, v2, v3, 0.2, epsilon) for v1, v2, v3 in transformed_values_5D]
    
    # 7D transformation
    transformed_values_7D = [u_to_v(v1, v2, v3, 0.2, epsilon) for v1, v2, v3 in transformed_values_6D]
    
    # 8D transformation
    transformed_values_8D = [u_to_v(v1, v2, v3, 0.2, epsilon) for v1, v2, v3 in transformed_values_7D]
    
    # 9D transformation
    transformed_values_9D = [u_to_v(v1, v2, v3, 0.2, epsilon) for v1, v2, v3 in transformed_values_8D]
    
    # 10D transformation
    transformed_values_10D = [u_to_v(v1, v2, v3, 0.2, epsilon) for v1, v2, v3 in transformed_values_9D]
    

    visualize_transformed_values_extended(cube_points, transformed_values_5D, transformed_values_6D, transformed_values_7D, transformed_values_8D, transformed_values_9D, transformed_values_10D)


    # Visualize the results
    # visualize_transformed_values(cube_points, transformed_values_4D_1, transformed_values_5D, transformed_values_8D)

if __name__ == "__main__":
    main()
