from direct.showbase.ShowBase import ShowBase
from panda3d.core import (
    CollisionTraverser, CollisionHandlerPusher, CollisionHandlerEvent,
    CollisionNode, CollisionSphere, ClockObject, Vec3, BitMask32
)
from direct.task import Task
import sys

globalClock = ClockObject.getGlobalClock()

class Game(ShowBase):
    def __init__(self):
        super().__init__()

        # Disable the default camera controls
        self.disableMouse()

        # Key mapping
        self.keys = {"forward": False, "backward": False, "left": False, "right": False}
        self.accept("w", self.update_key, ["forward", True])
        self.accept("w-up", self.update_key, ["forward", False])
        self.accept("s", self.update_key, ["backward", True])
        self.accept("s-up", self.update_key, ["backward", False])
        self.accept("a", self.update_key, ["left", True])
        self.accept("a-up", self.update_key, ["left", False])
        self.accept("d", self.update_key, ["right", True])
        self.accept("d-up", self.update_key, ["right", False])
        self.accept("escape", sys.exit)
        self.accept("mouse1", self.fire_weapon)

        # Set up the environment
        self.environment = self.loader.loadModel("models/environment")
        self.environment.reparentTo(self.render)
        self.environment.setScale(0.25)
        self.environment.setPos(-8, 42, 0)

        # Set up collision traverser and handlers
        self.cTrav = CollisionTraverser()
        self.pusher = CollisionHandlerPusher()
        self.eventHandler = CollisionHandlerEvent()
        self.eventHandler.addInPattern('%fn-into-%in')

        # Set up the player
        self.camera.setPos(0, 0, 2)
        self.cameraCollider = self.create_collider(self.camera, "player")
        self.camera.setPythonTag('collider', self.cameraCollider)  # Assign collider using setPythonTag
        self.cTrav.addCollider(self.cameraCollider, self.pusher)
        self.pusher.addCollider(self.cameraCollider, self.camera)

        # Set up enemies
        self.enemies = []
        self.load_enemy(pos=Vec3(10, 10, 0))
        self.load_enemy(pos=Vec3(-10, -5, 0))

        # Set up collision events
        self.accept('bullet-into-enemy', self.on_bullet_hit)
        self.accept('enemy-into-player', self.on_player_hit)

        # Task to update the game logic
        self.taskMgr.add(self.update, "update")

    def update_key(self, key, value):
        self.keys[key] = value

    def create_collider(self, obj, name):
        colliderNode = CollisionNode(name)
        colliderNode.addSolid(CollisionSphere(0, 0, 0, 1))
        # Set collision masks (optional but recommended)
        colliderNode.setFromCollideMask(BitMask32.bit(1))
        colliderNode.setIntoCollideMask(BitMask32.bit(1))
        collider = obj.attachNewNode(colliderNode)
        return collider

    def load_enemy(self, pos):
        enemy = self.loader.loadModel("models/panda")
        enemy.setScale(0.005)
        enemy.reparentTo(self.render)
        enemy.setPos(pos)
        enemy.setPythonTag('collider', self.create_collider(enemy, "enemy"))  # Use setPythonTag
        self.enemies.append(enemy)
        # Add enemy collider to traverser with pusher handler
        enemy_collider = enemy.getPythonTag('collider')
        self.cTrav.addCollider(enemy_collider, self.pusher)
        self.pusher.addCollider(enemy_collider, enemy)

    def fire_weapon(self):
        # Create a projectile
        bullet = self.loader.loadModel("models/misc/sphere")
        bullet.reparentTo(self.render)
        bullet.setScale(0.2)
        bullet.setPos(self.camera.getPos())
        bullet.setHpr(self.camera.getHpr())
        bullet.setPythonTag('collider', self.create_collider(bullet, "bullet"))  # Use setPythonTag
        bullet_collider = bullet.getPythonTag('collider')
        self.cTrav.addCollider(bullet_collider, self.eventHandler)
        # Add the bullet to the task manager
        self.taskMgr.add(self.move_bullet, "moveBullet", extraArgs=[bullet], appendTask=True)

    def move_bullet(self, bullet, task):
        speed = 50 * globalClock.getDt()
        bullet.setY(bullet, speed)
        # Remove the bullet if it goes too far
        if (bullet.getPos() - self.camera.getPos()).lengthSquared() > 10000:
            bullet.removeNode()
            return Task.done
        return Task.cont

    def on_bullet_hit(self, entry):
        bullet = entry.getFromNodePath().getParent()
        enemy = entry.getIntoNodePath().getParent()

        # Debugging: Print object names
        print(f"Bullet: {bullet.getName()}, Enemy: {enemy.getName()}")

        # Retrieve colliders using getPythonTag
        bullet_collider = bullet.getPythonTag('collider')
        enemy_collider = enemy.getPythonTag('collider')

        if bullet_collider and enemy_collider:
            if enemy in self.enemies:
                enemy.removeNode()
                self.enemies.remove(enemy)
            bullet.removeNode()
        else:
            print("One of the colliding objects lacks 'collider' attribute.")

    def on_player_hit(self, entry):
        enemy = entry.getFromNodePath().getParent()
        
        # Debugging: Print enemy name
        print(f"Enemy {enemy.getName()} hit the player.")
        
        # Retrieve collider using getPythonTag
        enemy_collider = enemy.getPythonTag('collider')

        if enemy_collider:
            # Handle player being hit, e.g., end game
            print("Player was hit!")
            sys.exit()
        else:
            print("Enemy lacks 'collider' attribute.")

    def update(self, task):
        dt = globalClock.getDt()
        speed = 10 * dt
        rotationSpeed = 100 * dt

        # Update player position
        if self.keys["forward"]:
            self.camera.setY(self.camera, speed)
        if self.keys["backward"]:
            self.camera.setY(self.camera, -speed)
        if self.keys["left"]:
            self.camera.setH(self.camera.getH() + rotationSpeed)
        if self.keys["right"]:
            self.camera.setH(self.camera.getH() - rotationSpeed)

        # Simple enemy AI
        for enemy in self.enemies:
            vectorToPlayer = self.camera.getPos() - enemy.getPos()
            vectorToPlayer.setZ(0)
            distance = vectorToPlayer.lengthSquared()
            if distance > 0.5:
                vectorToPlayer.normalize()
                enemy.setPos(enemy.getPos() + vectorToPlayer * dt * 2)
            else:
                print(f"Enemy {enemy.getName()} is too close to the player.")

        # Debugging: Check if all enemies have colliders
        for enemy in self.enemies:
            collider = enemy.getPythonTag('collider')
            if not collider:
                print(f"Enemy {enemy.getName()} is missing 'collider' attribute.")

        # Update collision detection
        self.cTrav.traverse(self.render)

        return Task.cont

game = Game()
game.run()