# main.py

import pygame
import sys
from config import WIDTH, HEIGHT, FPS, HUD_WIDTH, HUD_HEIGHT
from core.game import Game
from entities.happymeal import HappyMeal
from ui.hud import HUD, UnitButton, Button
from entities.healthy_enemy import Healthy
from ui.pause_menu import PauseMenu

def main():
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load("assets/sounds/day_time.mp3")
    pygame.mixer.music.set_volume(1.0)
    pygame.mixer.music.play(-1)

    VIRTUAL_WIDTH, VIRTUAL_HEIGHT = 1280, 720
    virtual_screen = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))

    fullscreen = False
    screen = pygame.display.set_mode((1280, 720))
    real_width, real_height = screen.get_size()
    pygame.display.set_caption("McDo vs Healthy")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)

    unit_images = {
        "Fontaine": pygame.image.load("assets/images/mcdo/foutain.png").convert_alpha(),
        "Nugget": pygame.image.load("assets/images/mcdo/nugget.jpg").convert_alpha(),
        "LanceurCornet": pygame.image.load("assets/images/mcdo/lanceur.jpg").convert_alpha(),
        "Shovel": pygame.image.load("assets/images/shovel.png").convert_alpha(),
        "LanceurFrite": pygame.image.load("assets/images/mcdo/lanceur_frite.png").convert_alpha()
    }

    bg = pygame.image.load("assets/images/bg.png").convert()
    button1 = UnitButton("Fontaine", unit_images["Fontaine"], 20, 30, cost=50, font=font)
    button2 = UnitButton("Nugget", unit_images["Nugget"], 20, 120, cost=100, font=font)
    button3 = UnitButton("LanceurCornet", unit_images["LanceurCornet"], 20, 210, cost=125, font=font)
    button4 = UnitButton("LanceurFrite", unit_images["LanceurFrite"], 20, 300, cost=75, font=font)
    button0 = UnitButton("Shovel", unit_images["Shovel"], x=20, y=390, cost="", font=font)

    image_happy_meal = pygame.image.load("assets/images/meal.png").convert_alpha()
    healthy_image = pygame.image.load("assets/images/healthy/orange.png").convert_alpha()
    hud = HUD([button1, button2, button3, button4, button0], width=HUD_WIDTH, height=HUD_HEIGHT, font=font)
    pygame.mixer.music.set_volume(1.0)
    selected_unit = None

    pause_menu = PauseMenu(screen, fullscreen)
    paused = False
    game = Game(virtual_screen)

    cooldowns = {}
    default_cooldowns = {}
    for name, info in game.mcdo_units.items():
        cooldowns[name] = 0
        default_cooldowns[name] = info["class"](0, 0).cooldown

    game_time = 0
    last_tick = pygame.time.get_ticks()
    last_spawn_time = 0

    while True:
        current_tick = pygame.time.get_ticks()
        delta = current_tick - last_tick
        last_tick = current_tick

        if not paused:
            game_time += delta

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    mx, my = pygame.mouse.get_pos()
                    scaled_x = mx * VIRTUAL_WIDTH / real_width
                    scaled_y = my * VIRTUAL_HEIGHT / real_height
                    game.happy_meal_group.add(HappyMeal(image=image_happy_meal, pos=(scaled_x, scaled_y)))

                elif event.key == pygame.K_F11:
                    fullscreen = not fullscreen
                    if fullscreen:
                        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((1280, 720))
                    real_width, real_height = screen.get_size()
                    pause_menu = PauseMenu(screen, fullscreen)

                elif event.key == pygame.K_ESCAPE:
                    paused = not paused

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = pygame.mouse.get_pos()
                scaled_x = mx * VIRTUAL_WIDTH / real_width
                scaled_y = my * VIRTUAL_HEIGHT / real_height
                pos = (scaled_x, scaled_y)

                print(pos)
                cell = game.grid.get_cell_from_pos(pos)
                unit_name = hud.handle_click(pos)

                if unit_name:
                    selected_unit = unit_name
                elif cell:
                    if selected_unit:
                        if selected_unit == "Shovel":
                            unit = game.grid.get_unit(cell[0], cell[1])
                            if unit:
                                game.grid.grid[cell[0]][cell[1]] = None
                                unit.kill()
                        elif game_time >= cooldowns[selected_unit]:
                            if game.try_place_unit(cell[0], cell[1], selected_unit):
                                cooldowns[selected_unit] = game_time + default_cooldowns[selected_unit]
                        selected_unit = None
                else:
                    selected_unit = None

                for hm in game.happy_meal_group:
                    if hm.rect.collidepoint(pos):
                        hm.collect()
                        game.happy_meal_group.remove(hm)
                        game.happymeal_points += 50
                        break

            

        if paused:
            pause_menu.draw()
            pygame.display.flip()
            for event in pygame.event.get():
                action = pause_menu.handle_event(event)
                if action == "resume":
                    paused = False
                elif action == "quit":
                    pygame.quit()
                    sys.exit()
                elif action == "toggle_fullscreen":
                    fullscreen = not fullscreen
                    if fullscreen:
                        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((1280, 720))
                    real_width, real_height = screen.get_size()
                    pause_menu = PauseMenu(screen, fullscreen)
                elif action == "volume_changed":
                    pygame.mixer.music.set_volume(pause_menu.get_volume())
            continue

        if game_time - last_spawn_time >= 2000:
            game.spawn_healthy(healthy_image)
            last_spawn_time = game_time

        game.update()
        game.happy_meal_group.update()
        game.projectile_group.update(game.healthy_group)
        game.healthy_group.update(game.grid)

        game.draw(bg)
        game.happy_meal_group.draw(virtual_screen)
        game.projectile_group.draw(virtual_screen)
        game.healthy_group.draw(virtual_screen)

        for button in hud.unit_buttons:
            if button.unit_name in cooldowns:
                remaining = max(0, cooldowns[button.unit_name] - game_time)
                button.set_cooldown(remaining, default_cooldowns[button.unit_name])

        hud.draw(virtual_screen, game.happymeal_points)

        if selected_unit and selected_unit in unit_images:
            mx, my = pygame.mouse.get_pos()
            scaled_x = mx * VIRTUAL_WIDTH / real_width
            scaled_y = my * VIRTUAL_HEIGHT / real_height
            virtual_screen.blit(pygame.transform.scale(unit_images[selected_unit], (64, 64)), (scaled_x - 32, scaled_y - 32))

        fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, (255, 255, 255))
        virtual_screen.blit(fps_text, (VIRTUAL_WIDTH - 100, VIRTUAL_HEIGHT - 30))

        scaled_surface = pygame.transform.scale(virtual_screen, (real_width, real_height))
        screen.blit(scaled_surface, (0, 0))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
