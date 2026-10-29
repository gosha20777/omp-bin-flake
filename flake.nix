{
  description = "Prebuilt standalone binaries for Oh My Pi (OMP)";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
  };

  outputs =
    { self, nixpkgs }:
    let
      sources = builtins.fromJSON (builtins.readFile ./sources.json);
      systems = [
        "x86_64-linux"
        "aarch64-linux"
        "aarch64-darwin"
      ];
      forAllSystems = nixpkgs.lib.genAttrs systems;
    in
    {
      packages = forAllSystems (
        system:
        let
          pkgs = nixpkgs.legacyPackages.${system};
          srcInfo = sources.${system} or (throw "Unsupported architecture: ${system}");
        in
        {
          default = pkgs.stdenv.mkDerivation {
            pname = "omp";
            version = sources.version;

            src = pkgs.fetchurl {
              inherit (srcInfo) url hash;
            };

            dontUnpack = true;
            dontStrip = true;

            installPhase = ''
              install -Dm755 $src $out/bin/omp
            '';

            meta = with pkgs.lib; {
              description = "Oh My Pi (OMP) coding agent (prebuilt standalone binary)";
              homepage = "https://github.com/can1357/oh-my-pi";
              license = licenses.mit;
              platforms = systems;
              mainProgram = "omp";
            };
          };
        }
      );
    };
}
