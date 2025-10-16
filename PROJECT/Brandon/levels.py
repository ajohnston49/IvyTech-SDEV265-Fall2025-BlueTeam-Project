# Level configuration for Tower Tactics

LEVELS = [
    {
        'id': 1,
        'name': 'Training Grounds',
        'platform_width': 400,
        'platform_height': 128,
        'enemies': [
            {'type': 'troll', 'position': 'center'}
        ],
        'terrain_color': 'color1',
        'terrain_layout': None,  # Simple flat platform
        'player_start': {'tile_col': 6, 'tile_row': 1}  # Center of platform
    },
    {
        'id': 1.5,
        'name': 'Mountain Steps',
        'platform_width': 512,
        'platform_height': 224,  # 7 rows * 32px = 224px
        'enemies': [
            {'type': 'troll', 'tile_col': 3, 'tile_row': 1},  # Left raised platform
            {'type': 'troll', 'tile_col': 11, 'tile_row': 1}   # Right raised platform
        ],
        'player_start': {'tile_col': 1, 'tile_row': 4},  # Base level near left edge
        'terrain_color': 'color2',
        'terrain_layout': [
            # Multi-level platform with lifted terrain and ramps
            # Each entry: (col, row, tile_type)
            # Platform height is 224px = 7 rows of 32px tiles (rows 0-6)

            # LOWEST LEVEL - Complete base (rows 3-5, 3 rows tall)
            # Top row of base
            (0, 3, 'top_corner_left'),
            (1, 3, 'top_middle'),
            (2, 3, 'top_middle'),
            (3, 3, 'top_middle'),
            (4, 3, 'top_middle'),
            (5, 3, 'top_middle'),
            (6, 3, 'top_middle'),
            (7, 3, 'top_middle'),
            (8, 3, 'top_middle'),
            (9, 3, 'top_middle'),
            (10, 3, 'top_middle'),
            (11, 3, 'top_middle'),
            (12, 3, 'top_middle'),
            (13, 3, 'top_middle'),
            (14, 3, 'top_middle'),
            (15, 3, 'top_corner_right'),
            # Middle row
            (0, 4, 'side_left'),
            (1, 4, 'middle'),
            (2, 4, 'middle'),
            (3, 4, 'middle'),
            (4, 4, 'middle'),
            (5, 4, 'middle'),
            (6, 4, 'middle'),
            (7, 4, 'middle'),
            (8, 4, 'middle'),
            (9, 4, 'middle'),
            (10, 4, 'middle'),
            (11, 4, 'middle'),
            (12, 4, 'middle'),
            (13, 4, 'middle'),
            (14, 4, 'middle'),
            (15, 4, 'side_right'),
            # Middle row
            (0, 5, 'side_left'),
            (1, 5, 'middle'),
            (2, 5, 'middle'),
            (3, 5, 'middle'),
            (4, 5, 'middle'),
            (5, 5, 'middle'),
            (6, 5, 'middle'),
            (7, 5, 'middle'),
            (8, 5, 'middle'),
            (9, 5, 'middle'),
            (10, 5, 'middle'),
            (11, 5, 'middle'),
            (12, 5, 'middle'),
            (13, 5, 'middle'),
            (14, 5, 'middle'),
            (15, 5, 'side_right'),
            # Bottom row (front edge)
            (0, 6, 'bottom_corner_left'),
            (1, 6, 'bottom_middle'),
            (2, 6, 'bottom_middle'),
            (3, 6, 'bottom_middle'),
            (4, 6, 'bottom_middle'),
            (5, 6, 'bottom_middle'),
            (6, 6, 'bottom_middle'),
            (7, 6, 'bottom_middle'),
            (8, 6, 'bottom_middle'),
            (9, 6, 'bottom_middle'),
            (10, 6, 'bottom_middle'),
            (11, 6, 'bottom_middle'),
            (12, 6, 'bottom_middle'),
            (13, 6, 'bottom_middle'),
            (14, 6, 'bottom_middle'),
            (15, 6, 'bottom_corner_right'),

            # RAMP TO LEFT PLATFORM - column 1 (ramp up from base to raised platform)
            (1, 2, 'ramp_left_top'),      # Top part of ramp
            (1, 3, 'ramp_left_bottom'),   # Bottom part of ramp on base level

            # RAISED PLATFORM 1 - Left side platform (columns 2-5, rows 1-2)
            # Top surface
            (2, 1, 'top_corner_left'),
            (3, 1, 'top_middle'),
            (4, 1, 'top_middle'),
            (5, 1, 'top_corner_right'),
            # Bottom layer - use middle for ramp connections
            (2, 2, 'middle'),  # Connects to ramp at (1, 2)
            (3, 2, 'middle'),
            (4, 2, 'middle'),
            (5, 2, 'middle'),
            # Lifted edges showing on base level
            (2, 3, 'lifted_left'),
            (3, 3, 'lifted_middle'),
            (4, 3, 'lifted_middle'),
            (5, 3, 'lifted_right'),

            # RAMP DOWN FROM LEFT PLATFORM - column 6
            (6, 2, 'ramp_right_top'),     # Top part on raised platform
            (6, 3, 'ramp_right_bottom'),  # Bottom part extends down

            # CENTER WALKWAY - columns 7-8, row 3 (on base level)
            (7, 3, 'middle'),
            (8, 3, 'middle'),

            # RAMP UP TO RIGHT PLATFORM - column 9
            (9, 2, 'ramp_left_top'),      # Top part of ramp
            (9, 3, 'ramp_left_bottom'),   # Bottom part on base level

            # RAISED PLATFORM 2 - Right side platform (columns 10-13, rows 1-2)
            # Top surface
            (10, 1, 'top_corner_left'),
            (11, 1, 'top_middle'),
            (12, 1, 'top_middle'),
            (13, 1, 'top_corner_right'),
            # Bottom layer - use middle for ramp connections
            (10, 2, 'middle'),  # Connects to ramp at (9, 2)
            (11, 2, 'middle'),
            (12, 2, 'middle'),
            (13, 2, 'middle'),
            # Lifted edges showing on base level
            (10, 3, 'lifted_left'),
            (11, 3, 'lifted_middle'),
            (12, 3, 'lifted_middle'),
            (13, 3, 'lifted_right'),

            # RAMP DOWN FROM RIGHT PLATFORM - column 14
            (14, 2, 'ramp_right_top'),    # Top part on raised platform
            (14, 3, 'ramp_right_bottom'), # Bottom part extends down
        ]
    },
    {
        'id': 2,
        'name': 'Forest Edge',
        'platform_width': 500,
        'platform_height': 160,
        'enemies': [
            {'type': 'troll', 'position': 'left'},
            {'type': 'troll', 'position': 'right'}
        ],
        'terrain_color': 'color2'
    },
    {
        'id': 3,
        'name': 'Mountain Path',
        'platform_width': 450,
        'platform_height': 128,
        'enemies': [
            {'type': 'troll', 'position': 'left'},
            {'type': 'troll', 'position': 'center'},
            {'type': 'troll', 'position': 'right'}
        ],
        'terrain_color': 'color3'
    },
    {
        'id': 4,
        'name': 'Dark Woods',
        'platform_width': 550,
        'platform_height': 192,
        'enemies': [
            {'type': 'troll', 'position': 'left'},
            {'type': 'troll', 'position': 'center-left'},
            {'type': 'troll', 'position': 'center-right'},
            {'type': 'troll', 'position': 'right'}
        ],
        'terrain_color': 'color1'
    },
    {
        'id': 5,
        'name': 'Troll Kingdom',
        'platform_width': 600,
        'platform_height': 192,
        'enemies': [
            {'type': 'troll', 'position': 'far-left'},
            {'type': 'troll', 'position': 'left'},
            {'type': 'troll', 'position': 'center'},
            {'type': 'troll', 'position': 'right'},
            {'type': 'troll', 'position': 'far-right'}
        ],
        'terrain_color': 'color2'
    }
]

def get_enemy_x_position(position, platform_x, platform_width):
    """Calculate enemy X position based on position name"""
    positions = {
        'far-left': platform_x + 80,
        'left': platform_x + platform_width * 0.25,
        'center-left': platform_x + platform_width * 0.33,
        'center': platform_x + platform_width * 0.5,
        'center-right': platform_x + platform_width * 0.66,
        'right': platform_x + platform_width * 0.75,
        'far-right': platform_x + platform_width - 80
    }
    return positions.get(position, platform_x + platform_width * 0.5)
