# main.py - 增强版动态粒子宇宙
import pygame
import sys
import random
import math
from particle import Particle

class ParticleUniverse:
    def __init__(self):
        # 初始化Pygame
        pygame.init()
        
        # 屏幕设置
        self.screen_width = 1200  # 更大的画布
        self.screen_height = 800
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Dynamic Particle Universe - Enhanced Interactive Art")
        
        # 颜色和字体
        self.background_color = (5, 5, 20)  # 更深的背景，增强对比度
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # 创建粒子系统 - 增加粒子数量
        self.particles = []
        self.num_particles = 500  # 增加到500个粒子
        
        # 帧计数器用于动画效果
        self.frame_count = 0
        
        # 初始化粒子
        self.reset_particles()
        
        # 互动模式设置
        self.attraction_modes = ["attract", "repel", "orbit", "color", "chaos"]
        self.current_mode = 0
        self.mouse_pressed = False
        
        # 背景星星
        self.stars = []
        self.generate_stars(100)  # 添加背景星星
        
        # 帧率控制
        self.clock = pygame.time.Clock()
        self.fps = 60
    
    def generate_stars(self, count):
        """生成背景星星"""
        for _ in range(count):
            self.stars.append({
                'x': random.randint(0, self.screen_width),
                'y': random.randint(0, self.screen_height),
                'size': random.uniform(0.5, 1.5),
                'brightness': random.uniform(0.3, 1.0)
            })
    
    def reset_particles(self):
        """重置所有粒子"""
        self.particles = []
        for _ in range(self.num_particles):
            x = random.randint(0, self.screen_width)
            y = random.randint(0, self.screen_height)
            self.particles.append(Particle(x, y, self.screen_width, self.screen_height))
    
    def handle_events(self):
        """处理所有用户输入事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # 空格键切换模式
                    self.current_mode = (self.current_mode + 1) % len(self.attraction_modes)
                    print(f"切换到模式: {self.attraction_modes[self.current_mode]}")
                elif event.key == pygame.K_r:
                    # R键重置粒子系统
                    self.reset_particles()
                    print("粒子系统已重置")
                elif event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    # 增加粒子数量
                    self.num_particles = min(1000, self.num_particles + 50)
                    self.reset_particles()
                    print(f"粒子数量增加到: {self.num_particles}")
                elif event.key == pygame.K_MINUS:
                    # 减少粒子数量
                    self.num_particles = max(100, self.num_particles - 50)
                    self.reset_particles()
                    print(f"粒子数量减少到: {self.num_particles}")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_pressed = True
                # 点击时在鼠标位置生成新粒子
                if event.button == 1:  # 左键
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    for _ in range(20):  # 一次生成20个新粒子
                        self.particles.append(Particle(
                            mouse_x + random.randint(-50, 50),
                            mouse_y + random.randint(-50, 50),
                            self.screen_width,
                            self.screen_height
                        ))
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_pressed = False
                
        return True
    
    def update(self):
        """更新粒子状态"""
        self.frame_count += 1
        mouse_x, mouse_y = pygame.mouse.get_pos()
        current_mode_name = self.attraction_modes[self.current_mode]
        
        # 更新所有粒子
        for particle in self.particles:
            particle.update(mouse_x, mouse_y, self.mouse_pressed, current_mode_name, self.frame_count)
    
    def draw(self):
        """绘制所有元素到屏幕"""
        # 绘制渐变背景
        self.screen.fill(self.background_color)
        
        # 绘制背景星星
        self.draw_stars()
        
        # 绘制所有粒子
        for particle in self.particles:
            # 为了性能，只绘制在屏幕范围内的粒子
            if (0 <= particle.x <= self.screen_width and 
                0 <= particle.y <= self.screen_height):
                current_size = particle.size  # 默认大小
                particle.draw(self.screen, current_size)
        
        # 绘制用户界面
        self.draw_ui()
        
        # 更新显示
        pygame.display.flip()
    
    def draw_stars(self):
        """绘制背景星星"""
        for star in self.stars:
            # 星星闪烁效果
            brightness = star['brightness'] * (0.8 + 0.2 * math.sin(self.frame_count * 0.05 + star['x'] * 0.01))
            color = (int(255 * brightness), int(255 * brightness), int(255 * brightness))
            pygame.draw.circle(
                self.screen, 
                color, 
                (int(star['x']), int(star['y'])), 
                star['size']
            )
    
    def draw_ui(self):
        """绘制用户界面元素"""
        # 显示当前模式
        mode_text = self.font.render(
            f"Mode: {self.attraction_modes[self.current_mode].upper()}", 
            True, (255, 255, 255)
        )
        self.screen.blit(mode_text, (20, 20))
        
        # 显示粒子数量
        count_text = self.small_font.render(
            f"Particles: {len(self.particles)}", 
            True, (200, 200, 200)
        )
        self.screen.blit(count_text, (20, 60))
        
        # 显示操作说明
        help_lines = [
            "SPACE: Change Mode | R: Reset | +/-: Adjust Particle Count",
            "MOUSE: Interact | CLICK: Create Particles | ESC: Quit"
        ]
        
        for i, line in enumerate(help_lines):
            help_text = self.small_font.render(line, True, (180, 180, 180))
            self.screen.blit(help_text, (20, self.screen_height - 60 + i * 25))
        
        # 绘制鼠标位置的视觉效果
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        # 鼠标光环
        for radius in [80, 60, 40, 20]:
            alpha = 100 - radius
            if alpha > 0:
                s = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
                pygame.draw.circle(s, (255, 255, 255, alpha), (radius, radius), radius, 1)
                self.screen.blit(s, (mouse_x - radius, mouse_y - radius))
    
    def run(self):
        """主循环"""
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.fps)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    universe = ParticleUniverse()
    universe.run()