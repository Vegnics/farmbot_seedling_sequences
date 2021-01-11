def usb_camera_photo():
    'Take a photo using a USB camera.'
    # Settings
    camera_port = 0      # default USB camera port
    max_port_num = 1     # highest port to try if not detected on port
    discard_frames = 10  # number of frames to discard for auto-adjust
    max_attempts = 5     # number of failed discard frames before quit
    image_width = int(WIDTH)
    image_height = int(HEIGHT)

    # Check USB devices for camera
    device_list_str = _get_usb_device_list()
    # Check video ports for camera
    video_ports = get_video_port_list()
    verbose_log('{} video ports detected: {}'.format(
        len(video_ports), ','.join(video_ports)))
    if len(video_ports) < 1:
        log('USB Camera not detected.{}'.format(device_list_str), 'error')
        return
    max_port_num = len(video_ports) - 1
    verbose_log('Adjusting max port number to {}.'.format(max_port_num))
    ret = False
    while camera_port <= max_port_num:
        camera_path = '/dev/video' + str(camera_port)
        verbose_log('Trying {}'.format(camera_path))
        if not os.path.exists(camera_path):
            verbose_log('{} missing'.format(camera_path))
            camera_port += 1
            continue

        # Close process using camera (if open)
        _check_camera_availability(camera_path)

        # Open the camera
        camera = _open_camera(camera_port)
        if camera is None:
            return

        verbose_log('Adjusting image with test captures...')
        # Set image size
        _adjust_settings(camera, image_width, image_height)
        # Capture test frame
        ret, _ = _capture_usb_image(camera)
        if not ret:
            camera.release()
            verbose_log('Couldn\'t get frame from {}'.format(camera_path))
            camera_port += 1
            continue
        break
    if not ret:
        _log_no_image()
        return
    verbose_log('First test frame captured.')
    # Let camera adjust
    failed_attempts = 0
    for _ in range(discard_frames):
        if not camera.grab():
            verbose_log('Could not get frame.')
            failed_attempts += 1
        if failed_attempts >= max_attempts:
            break
        sleep(0.1)

    # Take a photo
    verbose_log('Taking photo...')
    ret, image = _capture_usb_image(camera)

    # Close the camera
    camera.release()

    # Output
    if ret:  # an image has been returned by the camera
        verbose_log('Photo captured.')
        save_image(image)
    else:  # no image has been returned by the camera
        _log_no_image()
