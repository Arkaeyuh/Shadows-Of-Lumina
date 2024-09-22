class CombatSystem:
    def __init__(self, player, enemies):
        self.player = player
        self.enemies = enemies

    def attack(self, target):
        damage = 20 # Example damage value
        target.health -= damage
    
    def check_collisions(self):
        for enemy in self.enemies:
            if self.player.rect.colliderect(enemy.rect):
                self.attack(enemy)
