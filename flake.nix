{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs =
    { nixpkgs, ... }:
    let
      supportedSystems = [
        "x86_64-linux"
        "aarch64-darwin"
      ];
      forAllSystems = f: nixpkgs.lib.genAttrs supportedSystems (system: f system);
    in
    {
      devShells = forAllSystems (
        system:
        let
          pkgs = nixpkgs.legacyPackages.${system};
          isLinux = pkgs.stdenv.hostPlatform.isLinux;
        in
        {
          default = pkgs.mkShell {
            buildInputs =
              with pkgs;
              [
                uv
                ruff
                python313
              ];

            # Native libraries required by cadquery-ocp pre-built wheels (Linux only).
            # macOS wheels bundle their own dependencies via dyld.
            LD_LIBRARY_PATH = pkgs.lib.optionalString isLinux (
              pkgs.lib.makeLibraryPath (
                with pkgs;
                [
                  stdenv.cc.cc.lib # libstdc++
                  libGL
                  libx11
                  expat
                  zlib
                ]
              )
            );
          };
        }
      );
    };
}
