# Maintainer: george <rpubaddr0 {at} gmail [dot] com>

pkgname=python2-ccr
pkgver=0.2
pkgrel=1
pkgdesc='A python library for accessing and working with the CCR.'
arch=('i686' 'x86_64')
url='http://github.com/ccr-tools/python-ccr/'
license=('GPLv2 or any later version')
depends=('python2')
makedepends=('python-distribute')
source=("http://cloud.github.com/ccr-tools/python-ccr/somethingelse/${pkgname}-${pkgver}.tar.gz")
sha256sums=('a')

package() {
  cd "${pkgname}-${pkgver}"
  export PYTHONPATH="$PYTHONPATH:${pkgdir}/usr/lib/python2.7/site-packages/"
  install -dm755 "${pkgdir}/usr/lib/python2.7/site-packages"
  python setup.py install --prefix="${pkgdir}/usr"
}
