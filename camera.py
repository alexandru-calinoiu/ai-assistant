import pygame
import pygame.camera

pygame.init()
pygame.camera.init()
print(pygame.camera.list_cameras())

cam = pygame.camera.Camera('/dev/video0', (320,240), 'RGB')

cam.start()
img = cam.get_image()
pygame.image.save(img, 'capture.jpg')
cam.stop()
