import pygame
import sys

class Node:
    def __init__(self):
        self.keys = []
        self.children = []

class TwoFourTree:
    def __init__(self):
        self.root = Node()

    def insert(self, key):
        if len(self.root.keys) == 3:
            self._insert_non_full(self.root, key)
            new_root = Node()
            new_root.children.append(self.root)
            for current_node in new_root.children:
                print(current_node.keys, end=", ")
            self.split_child(new_root, 0)
            self.root = new_root
        else:
            self._insert_non_full(self.root, key)

    def _insert_non_full(self, node, key):
        if not node.children:
            node.keys.append(key)
            node.keys.sort()
        else:
            i = len(node.keys) - 1
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1
            if len(node.children[i].keys) == 3:
                self._insert_non_full(node.children[i], key)
                self.split_child(node, i)
                if key > node.keys[i]:
                    i += 1
            else:
                self._insert_non_full(node.children[i], key)
                for current_node in node.children:
                    print(current_node.keys, end=", ")

    def split_child(self, parent, index):
        node = parent.children[index]
        new_node = Node()
        parent.children.insert(index + 1, new_node)
        for current_node in parent.children:
            print(current_node.keys, end=", ")
        parent.keys.insert(index, node.keys[2])
        new_node.keys = node.keys[3:]
        node.keys = node.keys[:2]
        if node.children:
            new_node.children = node.children[2:]
            node.children = node.children[:2]

def draw_tree(screen, font, node, x, y, dx):
    if node:
        keys_text = ' | '.join(map(str, node.keys))
        text = font.render(keys_text, True, (0, 0, 0))
        screen.blit(text, (x, y))
        
        if node.children:
            for i, child in enumerate(node.children):
                child_x = x + (i - len(node.children) / 2) * dx
                pygame.draw.line(screen, (0, 0, 0), (x + 20, y + 20), (child_x + 20, y + 60))
                draw_tree(screen, font, child, child_x, y + 60, dx / 2)

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("2-4 Tree Visualization")
    font = pygame.font.SysFont(None, 24)
    clock = pygame.time.Clock()

    tree = TwoFourTree()
    input_text = ''
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if input_text.isdigit():
                        tree.insert(int(input_text))
                        input_text = ''
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

        screen.fill((255, 255, 255))
        draw_tree(screen, font, tree.root, 400, 50, 200)
        
        # Display the current input
        input_surface = font.render(f'Input: {input_text}', True, (0, 0, 0))
        screen.blit(input_surface, (10, 10))
        
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
