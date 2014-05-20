# Build and install the Python3 bindings for KDE4.
wget http://download.kde.org/stable/4.13.1/src/pykde4-4.13.1.tar.xz
tar xf pykde4-4.13.1.tar.xz
mkdir build && cd build
export PYTHONDONTWRITEBYTECODE="TRUE"
cmake ../pykde4-4.13.1 \
    -DCMAKE_BUILD_TYPE=Release \
    -DKDE4_BUILD_TESTS=OFF \
    -DCMAKE_INSTALL_PREFIX=/usr \
    -DPYTHON_EXECUTABLE=/usr/bin/python3 \
    -DPYTHON_LIBRARY=/usr/lib/libpython3.4m.so.1.0 \
    -DPYKDEUIC4_ALTINSTALL=TRUE \
    -DWITH_Nepomuk=OFF \
    -DWITH_Soprano=OFF
make
sudo make install
sudo ln -s /usr/bin/pykdeuic4-3.4 /usr/bin/pykdeuic4
