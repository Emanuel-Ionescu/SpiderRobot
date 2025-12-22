"""
Web GUI module for SpiderRobot control interface.

This module provides a Flask-based web interface for:
- Real-time video streaming from a multiprocessing queue
- Robot control via 4 interactive buttons
- REST API endpoints for command handling

Usage:
    from web_gui import run_server
    from multiprocessing import Queue, Process
    
    frame_queue = Queue(maxsize=2)
    server_process = Process(target=run_server, args=(frame_queue,))
    server_process.start()
"""

from .server import run_server, set_frame_queue, app

__all__ = ['run_server', 'set_frame_queue', 'app']
__version__ = '1.0.0'
