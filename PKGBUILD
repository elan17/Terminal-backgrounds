
# Maintainer: Juan Toca <elan17.programacion@gmail.com>
pkgname=terminal-backgrounds-git
pkgver=r6.a8877fd
pkgrel=1
pkgdesc="A set of terminal live-wallpapers"
arch=('any')
url="https://github.com/elan17/Terminal-backgrounds"
license=('GPL3')
groups=()
depends=()
makedepends=('git' 'python')
provides=("${pkgname%-VCS}")
conflicts=("${pkgname%-VCS}")
replaces=()
backup=()
options=(!emptydirs)
install=
source=('terminal-backgrounds-git::git+https://github.com/elan17/Terminal-backgrounds#branch=master')
noextract=()
md5sums=('SKIP')

pkgver() {
  cd "$pkgname"
  printf "r%s.%s" "$(git rev-list --count HEAD)" "$(git rev-parse --short HEAD)"
}

package() {
	cd "$srcdir/$pkgname"
  	install -Dm 755 ./snakes/snakes.py "${pkgdir}/usr/bin/wp-snakes"
  	install -Dm 644 ./snakes/LICENSE "${pkgdir}/usr/share/doc/${pkgname}/wp-snakes/LICENSE"
  	install -Dm 755 ./Game\ Of\ Life/game_of_life.py "${pkgdir}/usr/bin/wp-livegame"
  	install -Dm 644 ./Game\ Of\ Life/LICENSE "${pkgdir}/usr/share/doc/${pkgname}/wp-livegame/LICENSE"
  	install -Dm 755 ./maze/maze.py "${pkgdir}/usr/bin/wp-maze"
  	install -Dm 644 ./maze/LICENSE "${pkgdir}/usr/share/doc/${pkgname}/wp-maze/LICENSE"
}
