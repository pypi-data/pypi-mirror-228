# This file is part of Snagboot
# Copyright (C) 2023 Bootlin
#
# Written by Romain Gantois <romain.gantois@bootlin.com> in 2023.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from snagrecover.protocols import dfu
import logging
logger = logging.getLogger("snagflash")
from snagflash.utils import cli_error, get_usb, reset_usb
from usb.core import Device

def dfu_detach(dev: Device, altsetting: int = 0):
	print("Sending DFU detach command...")
	dfu_cmd = dfu.DFU(dev, stm32=False)
	dfu_cmd.get_status()
	dfu_cmd.detach(altsetting)
	print("Done")

def dfu_download(dev: Device, altsetting: int, path: str):
	with open(path, "rb") as file:
		blob = file.read(-1)
	size = len(blob)
	print(f"Downloading {path} to altsetting {altsetting}...")
	logger.debug(f"DFU config altsetting:{altsetting} size:0x{size:x} path:{path}")
	dfu_cmd = dfu.DFU(dev, stm32=False)
	dfu_cmd.get_status()
	dfu_cmd.download_and_run(blob, altsetting, 0, size, show_progress=True)
	dfu_cmd.get_status()
	print("Done")

def dfu_reset(dev: Device):
	print("Sending DFU reset command...")
	reset_usb(dev)
	print("Done")

def dfu_cli(args):
	if args.dfu_config is None and not args.dfu_detach and not args.dfu_reset:
		cli_error("missing command line argument --dfu-config")
	if (args.port is None) or (":" not in args.port):
		cli_error("missing command line argument --port [vid:pid]")
	dev_addr = args.port.split(":")
	vid  = int(dev_addr[0], 16)
	pid = int(dev_addr[1], 16)
	dev = get_usb(vid, pid)
	dev.default_timeout = int(args.timeout)
	altsetting = 0
	if args.dfu_config:
		for dfu_config in args.dfu_config:
			(altsetting,sep,path) = dfu_config.partition(":")
			altsetting = int(altsetting)
			dfu_download(dev, altsetting, path)
	if not args.dfu_keep or args.dfu_detach or args.dfu_reset:
		dfu_detach(dev, altsetting)
	if args.dfu_reset:
		dfu_reset(dev)
