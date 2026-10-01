import pygame

BG = (8, 10, 18)
PANEL = (17, 21, 34)
PANEL_2 = (25, 30, 47)

TEXT = (239, 242, 248)
MUTED = (157, 166, 186)

ACCENT = (110, 231, 183)
ACCENT_2 = (99, 102, 241)

DANGER = (248, 113, 113)


def font(size, bold=False):
    return pygame.font.SysFont("segoeui", size, bold=bold)


def draw_background(screen):
    screen.fill(BG)

    w, h = screen.get_size()

    # Fundo com círculos concêntricos
    for i in range(10):
        alpha = max(0, 26 - i * 2)

        surface = pygame.Surface((w, h), pygame.SRCALPHA)

        pygame.draw.circle(
            surface,
            (*ACCENT_2, alpha),
            (w // 2, h // 2),
            240 + i * 30
        )

        screen.blit(surface, (0, 0))


def draw_header(screen, title, subtitle=""):
    title_img = font(34, True).render(title, True, TEXT)
    screen.blit(title_img, (55, 34))

    if subtitle:
        sub_img = font(16).render(subtitle, True, MUTED)
        screen.blit(sub_img, (58, 77))


def button(screen, rect, label, selected=False, hover=False):

    # Cor normal
    if selected:
        color = ACCENT
        text_color = BG

    # Cor quando o mouse está sobre o botão
    elif hover:
        color = (40, 48, 72)
        text_color = ACCENT

    # Cor padrão
    else:
        color = PANEL_2
        text_color = TEXT

    pygame.draw.rect(
        screen,
        color,
        rect,
        border_radius=14
    )

    # Borda
    border_color = ACCENT if hover or selected else (48, 55, 78)

    pygame.draw.rect(
        screen,
        border_color,
        rect,
        width=2 if hover else 1,
        border_radius=14
    )

    # Texto
    img = font(19, True).render(
        label,
        True,
        text_color
    )

    screen.blit(
        img,
        img.get_rect(center=rect.center)
    )