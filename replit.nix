{pkgs}: {
  deps = [
    pkgs.libxcrypt
    pkgs.ffmpeg-full
    pkgs.postgresql
    pkgs.openssl
  ];
}
