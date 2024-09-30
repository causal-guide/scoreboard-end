from endstone import Player
from endstone.plugin import Plugin
from endstone.scoreboard import Scoreboard, Criteria, DisplaySlot

class ScoreboardExample(Plugin):
    def on_enable(self) -> None:
        self.logger.info("Scoreboard Plugin Enabled!")
        self.register_events(self)  # Register event listeners

    def get_player_score(self, player: Player, objective_name: str) -> int:
        # Get the scoreboard
        scoreboard = player.scoreboard

        # Retrieve the objective by name
        objective = scoreboard.get_objective(objective_name)
        if objective is None:
            self.logger.info(f"Objective {objective_name} does not exist!")
            return 0

        # Get the player's score
        score = objective.get_score(player)
        return score.value

    def set_player_score(self, player: Player, objective_name: str, value: int) -> None:
        # Get the scoreboard
        scoreboard = player.scoreboard

        # Retrieve or create the objective
        objective = scoreboard.get_objective(objective_name)
        if objective is None:
            objective = scoreboard.add_objective(
                name=objective_name,
                criteria=Criteria.DUMMY,
                display_name="Player Score"
            )

        # Set the player's score
        score = objective.get_score(player)
        score.value = value
        self.logger.info(f"Set score for {player.name} to {value}")

    def remove_player_score(self, player: Player, objective_name: str) -> None:
        # Get the scoreboard
        scoreboard = player.scoreboard

        # Reset the player's score for the specific objective
        scoreboard.reset_scores(player)
        self.logger.info(f"Removed score for {player.name} from {objective_name}")

    @event_handler
    def on_player_join(self, event):
        player = event.player

        # Create or update player's score on join
        self.set_player_score(player, "example_objective", 10)
        player.send_message(f"Welcome, {player.name}! Your score has been set to 10.")

        # Display current score
        current_score = self.get_player_score(player, "example_objective")
        player.send_message(f"Your current score is {current_score}.")
