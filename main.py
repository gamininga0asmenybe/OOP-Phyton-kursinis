import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, UI_FONT_PATH
from levels import LevelFactory


def draw_text(surface, text, font, color, center_pos):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=center_pos)
    surface.blit(text_surface, text_rect)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Mano Žaidimas")
    clock = pygame.time.Clock()

    def show_intro_screen():
        screen.fill((0, 0, 0))
        try:
            intro_font = pygame.font.Font(UI_FONT_PATH, 48)
        except (pygame.error, FileNotFoundError):
            print(
                f"Warning: Could not load font '{UI_FONT_PATH}'. "
                "Using default for intro."
            )
            intro_font = pygame.font.SysFont(None, 60)

        draw_text(
            screen,
            "Sveiki atvykę į žaidimą!",
            intro_font,
            (255, 255, 255),
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
        )
        pygame.display.flip()
        pygame.time.wait(5000)

    show_intro_screen()

    level_types = ["platform", "maze", "puzzle"]
    current_level_index = 0
    level_factory = LevelFactory()

    def load_level(index):
        if index < len(level_types):
            level_type = level_types[index]
            print(f"Loading level {index + 1}: {level_type}")
            return level_factory.create_level(level_type)
        print("All levels completed!")
        return None

    current_level = load_level(current_level_index)

    if not current_level:
        print("ERROR: Could not create the initial level.")
        pygame.quit()
        return

    running = True
    show_end_screen = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if current_level and not show_end_screen:
            keys = pygame.key.get_pressed()
            level_status = current_level.update(keys)

            if level_status == "completed":
                print(
                    f"Level {current_level_index + 1} "
                    f"({level_types[current_level_index]}) completed!"
                )
                current_level_index += 1
                current_level = load_level(current_level_index)
                if not current_level:
                    running = False

            elif level_status == "restart":
                print(f"Perkraunamas lygis {current_level_index + 1}")
                current_level = load_level(current_level_index)
                if not current_level:
                    print("KLAIDA: Nepavyko perkrauti lygio.")
                    running = False

            elif level_status == "show_end_message":
                print("Žaidimo pabaiga - surinktos visos žvaigždės!")
                show_end_screen = True
                current_level = None

        elif not current_level and not show_end_screen:
            running = False

        screen.fill((0, 0, 0))
        if current_level:
            current_level.draw(screen)
        elif show_end_screen:
            try:
                end_font = pygame.font.Font(UI_FONT_PATH, 60)
            except (pygame.error, FileNotFoundError):
                end_font = pygame.font.SysFont(None, 72)
            draw_text(
                screen,
                "Žaidimo pabaiga",
                end_font,
                (255, 0, 0),
                (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
            )

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
