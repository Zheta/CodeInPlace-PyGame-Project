# Import local files
from zelda_utilities.constants import *
vec = pygame.math.Vector2


def collide_with_walls(sprite, group, direction):
    if direction == 'x':
        hits = pygame.sprite.spritecollide(sprite, group, False, collided=collide_hit_rect)
        if hits:
            # https://www.youtube.com/watch?v=-9bXcSjuN28&list=PLsk-HSGFjnaH5yghzu7PcOzm9NhsW0Urw&index=46
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if direction == 'y':
        hits = pygame.sprite.spritecollide(sprite, group, False, collided=collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y


# callback function https://youtu.be/5M_-cJP5rk8?t=1128
# do NOT include the () in the callback, just:   collided=collide_hit_rect
def collide_hit_rect(one, two):
    if one is not two:
        return one.hit_rect.colliderect(two.rect)
    else:
        return False

# def collide_hit_rect(sprite1, sprite2):
#     if sprite1 is not sprite2:
#         return sprite1.hit_rect.colliderect(sprite2.hit_rect)
#     else:
#         return False
