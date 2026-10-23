class Observer:
    @staticmethod
    def notify_player_death(player):
        # set_player_dead(player)
        pass

    @staticmethod
    def notify_team_has_no_members(team):
        print(f"Team {team} has no members!")

    @staticmethod
    def notify_next_period(period):
        print(f"The period {period} is started!")