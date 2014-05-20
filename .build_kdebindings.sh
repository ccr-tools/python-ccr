# Build and install the Python3 bindings for KDE4.
version=4.8.5
wget http://download.kde.org/stable/${version}/src/pykde4-${version}.tar.xz
tar xf pykde4-${version}.tar.xz
mkdir build && cd build
export PYTHONDONTWRITEBYTECODE="TRUE"
cmake ../pykde4-${version} \
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
