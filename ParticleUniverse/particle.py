# particle.py - 增强版粒子类
import pygame
import random
import math

class Particle:
    def __init__(self, x, y, screen_width, screen_height):
        self.x = x
        self.y = y
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # 速度属性 - 更丰富的初始速度
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)
        
        # 外观属性 - 更多样化
        self.size = random.randint(3, 8)  # 更大的粒子范围
        self.base_color = (
            random.randint(150, 255),  # 更亮的颜色
            random.randint(150, 255),
            random.randint(150, 255)
        )
        self.current_color = self.base_color
        self.glow_size = self.size + random.randint(2, 5)  # 光晕效果
        
        # 粒子类型 - 增加多样性
        self.particle_type = random.choice(["normal", "fast", "glow", "trail"])
        
        # 生命周期和脉冲效果
        self.life = 255
        self.pulse_speed = random.uniform(0.02, 0.05)
        self.pulse_offset = random.uniform(0, math.pi * 2)
        self.pulse_size = random.uniform(0.5, 1.5)
        
        # 轨迹效果
        self.trail_positions = []
        self.max_trail_length = random.randint(5, 15)
    
    def update(self, mouse_x, mouse_y, mouse_pressed, attraction_mode, frame_count=None):
        # 兼容：如果调用方没有传入 frame_count，则使用 0
        if frame_count is None:
            frame_count = 0

        # 保存历史位置用于轨迹
        if self.particle_type == "trail":
            self.trail_positions.append((self.x, self.y))
            if len(self.trail_positions) > self.max_trail_length:
                self.trail_positions.pop(0)
        
        # 计算粒子与鼠标的距离
        dx = mouse_x - self.x
        dy = mouse_y - self.y
        distance = max(math.sqrt(dx*dx + dy*dy), 0.1)
        
        # 脉冲效果 - 粒子大小会呼吸
        pulse = math.sin(frame_count * self.pulse_speed + self.pulse_offset) * self.pulse_size
        current_size = max(1, self.size + pulse)
        
        # 根据互动模式调整行为
        interaction_strength = 1.0
        if distance < 200:  # 扩大互动范围
            if attraction_mode == "attract":
                force = 0.8 / distance
                self.vx += dx * force * 0.08
                self.vy += dy * force * 0.08
                interaction_strength = 1.5
                
            elif attraction_mode == "repel":
                force = 1.5 / distance
                self.vx -= dx * force * 0.05
                self.vy -= dy * force * 0.05
                interaction_strength = 1.5
                
            elif attraction_mode == "orbit":
                force = 15.0 / (distance * distance)
                self.vx += -dy * force * 0.015
                self.vy += dx * force * 0.015
                interaction_strength = 1.3
                
            elif attraction_mode == "color":
                # 根据距离和角度改变颜色
                angle = math.atan2(dy, dx)
                color_factor = min(1.0, 200 / distance)
                
                r = int(self.base_color[0] * (1 - color_factor) + 
                       (128 + 127 * math.sin(angle)) * color_factor)
                g = int(self.base_color[1] * (1 - color_factor) + 
                       (128 + 127 * math.sin(angle + 2)) * color_factor)
                b = int(self.base_color[2] * (1 - color_factor) + 
                       (128 + 127 * math.sin(angle + 4)) * color_factor)
                
                self.current_color = (
                    max(0, min(255, r)),
                    max(0, min(255, g)),
                    max(0, min(255, b))
                )
                interaction_strength = 1.2
                
            elif attraction_mode == "chaos":
                # 混沌模式 - 更强烈的随机行为
                if random.random() < 0.15:
                    chaos_type = random.choice(["attract", "repel", "spin", "teleport"])
                    if chaos_type == "attract":
                        force = 0.5 / distance
                        self.vx += dx * force * 0.2
                        self.vy += dy * force * 0.2
                    elif chaos_type == "repel":
                        force = 2.0 / distance
                        self.vx -= dx * force * 0.15
                        self.vy -= dy * force * 0.15
                    elif chaos_type == "spin":
                        force = 20.0 / (distance * distance)
                        self.vx += -dy * force * 0.1
                        self.vy += dx * force * 0.1
                    elif chaos_type == "teleport":
                        if random.random() < 0.1:
                            self.x = random.randint(0, self.screen_width)
                            self.y = random.randint(0, self.screen_height)
                interaction_strength = 2.0
            
            # 鼠标按下时增强效果
            if mouse_pressed:
                interaction_strength *= 1.5
                
                if attraction_mode == "color":
                    # 鼠标按下时产生颜色爆炸
                    self.current_color = (
                        random.randint(0, 255),
                        random.randint(0, 255),
                        random.randint(0, 255)
                    )
        
        # 根据粒子类型调整行为
        if self.particle_type == "fast":
            self.vx *= 1.05
            self.vy *= 1.05
        elif self.particle_type == "glow":
            self.glow_size = current_size + 5 + math.sin(frame_count * 0.1) * 3
        
        # 添加随机运动 - 根据互动强度调整
        random_strength = 0.1 * interaction_strength
        self.vx += random.uniform(-random_strength, random_strength)
        self.vy += random.uniform(-random_strength, random_strength)
        
        # 限制速度
        speed = math.sqrt(self.vx*self.vx + self.vy*self.vy)
        max_speed = 8 if self.particle_type == "fast" else 6
        if speed > max_speed:
            self.vx = (self.vx / speed) * max_speed
            self.vy = (self.vy / speed) * max_speed
        
        # 更新位置
        self.x += self.vx
        self.y += self.vy
        
        # 更柔和的边界检查
        border_margin = 20
        if self.x < -border_margin or self.x > self.screen_width + border_margin:
            self.vx *= -0.9
        if self.y < -border_margin or self.y > self.screen_height + border_margin:
            self.vy *= -0.9
            
        self.x = max(-border_margin, min(self.screen_width + border_margin, self.x))
        self.y = max(-border_margin, min(self.screen_height + border_margin, self.y))
        
        # 缓慢恢复颜色（如果不是颜色模式）
        if attraction_mode != "color" and self.current_color != self.base_color:
            self.current_color = tuple(
                int(self.current_color[i] + (self.base_color[i] - self.current_color[i]) * 0.05)
                for i in range(3)
            )
        
        return current_size
    
    def draw(self, screen, current_size):
        # 绘制轨迹
        if self.particle_type == "trail" and len(self.trail_positions) > 1:
            for i in range(1, len(self.trail_positions)):
                alpha = int(255 * i / len(self.trail_positions))
                pos = self.trail_positions[i]
                prev_pos = self.trail_positions[i-1]
                
                trail_color = (
                    self.current_color[0],
                    self.current_color[1], 
                    self.current_color[2],
                    alpha
                )
                
                # 使用pygame.draw.line绘制轨迹线
                pygame.draw.line(
                    screen, 
                    trail_color, 
                    (int(pos[0]), int(pos[1])),
                    (int(prev_pos[0]), int(prev_pos[1])),
                    max(1, int(current_size * 0.5))
                )
        
        # 绘制光晕效果
        if self.particle_type == "glow":
            glow_surface = pygame.Surface((self.glow_size*2, self.glow_size*2), pygame.SRCALPHA)
            pygame.draw.circle(
                glow_surface, 
                (*self.current_color, 100),  # 半透明
                (self.glow_size, self.glow_size), 
                self.glow_size
            )
            screen.blit(glow_surface, (self.x - self.glow_size, self.y - self.glow_size))
        
        # 绘制粒子主体
        pygame.draw.circle(screen, self.current_color, (int(self.x), int(self.y)), int(current_size))
        
        # 为快速粒子添加速度线
        if self.particle_type == "fast":
            speed = math.sqrt(self.vx*self.vx + self.vy*self.vy)
            if speed > 3:
                end_x = int(self.x - self.vx * 2)
                end_y = int(self.y - self.vy * 2)
                pygame.draw.line(
                    screen, 
                    self.current_color, 
                    (int(self.x), int(self.y)), 
                    (end_x, end_y), 
                    max(1, int(current_size * 0.7))
                )