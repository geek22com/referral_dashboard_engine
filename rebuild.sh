#!/bin/bash
dpkg -r frontend
debclean
debuild -uc -us -b

