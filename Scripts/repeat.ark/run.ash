template_screen_size(1600, 900)
set_skip_img('network_err1.png | level_up.png', (0.5, 0.5))
set_skip_img('network_err2.png', 'ok_red.png')
set_stop_img('network_err3.png', 'ok_black.png')
click('st1_blue.png | st1_pink.png')
click('st2.png')
click('mission_accomplish.png', frequency=7)