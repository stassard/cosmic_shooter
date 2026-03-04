import sys
import pygame
from constants import *
from alien import Alien
from fighter import Fighter
from old import game_score_text
from rocket import Rocket

class Game:
    def __init__(self):
        pygame.display.set_caption(GAME_CAPTION)
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.screen_feel_color = SCREEN_FEEL_COLOR
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.game_font = pygame.font.Font(None, 30)
        self.game_score = 0

        self.fighter = Fighter()
        self.alien = Alien()
        self.rocket = Rocket(self.fighter)

        self.game_is_running = True

    def run(self):
        while self.game_is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                self.handle_key_events(event)

            self.update_game_state()
            self.draw_screen()
        self.show_game_over()

    def handle_key_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.fighter.move_left()
            if event.key == pygame.K_RIGHT :
                self.fighter.move_right()
            if event.key == pygame.K_SPACE:
                self.rocket.fire()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.fighter.stop_moving()
            if event.key == pygame.K_RIGHT:
                self.fighter.stop_moving()

    def update_game_state(self):
        self.fighter.update_position()
        self.alien.update_position()
        self.rocket.update_position()

        if self.rocket.is_out_of_screen():
            self.rocket.reset()

        if self.rocket.is_collision(self.alien):
            self.rocket.reset()
            self.alien.reset()
            self.game_score += 1

        if self.alien.has_reached_fighter(self.fighter):
            self.game_is_running = False

    def draw_screen(self):
        self.screen.fill(self.screen_feel_color)
        self.screen.blit(self.fighter.image, (self.fighter.x, self.fighter.y))
        self.screen.blit(self.alien.image, (self.alien.x, self.alien.y))
        if self.rocket.was_fired:
            self.screen.blit(self.rocket.image, (self.rocket.x, self.rocket.y))
        self.show_game_score()
        pygame.display.update()

    def show_game_score(self):
        game_score_text = self.game_font.render(f"Your score: {self.game_score}", True, "white")
        self.screen.blit(game_score_text, (20, 20))

    def show_game_over(self):
        game_over_text = self.game_font.render("GAME OVER", True, "white")
        game_over_rectangle = game_over_text.get_rect()
        game_over_rectangle.center = (self.screen_width / 2, self.screen_height / 2)
        self.screen.blit(game_over_text, game_over_rectangle)
        pygame.display.update()
        pygame.time.wait(5000)