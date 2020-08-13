#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/legoboost/catkin_ws/src/universal_robot/ur_driver"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/legoboost/catkin_ws/install/lib/python3/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/legoboost/catkin_ws/install/lib/python3/dist-packages:/home/legoboost/catkin_ws/build/lib/python3/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/legoboost/catkin_ws/build" \
    "/usr/bin/python3" \
    "/home/legoboost/catkin_ws/src/universal_robot/ur_driver/setup.py" \
     \
    build --build-base "/home/legoboost/catkin_ws/build/universal_robot/ur_driver" \
    install \
    --root="${DESTDIR-/}" \
    --install-layout=deb --prefix="/home/legoboost/catkin_ws/install" --install-scripts="/home/legoboost/catkin_ws/install/bin"
