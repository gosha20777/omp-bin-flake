# omp-bin-flake

Prebuilt standalone binaries for [Oh My Pi (OMP)](https://github.com/can1357/oh-my-pi).

Automatically tracks official GitHub Releases of `can1357/oh-my-pi` via GitHub Actions and provides instant, zero-compilation Nix flake packages for:
- `x86_64-linux`
- `aarch64-linux` (including 16K page size support for Apple Silicon / Asahi Linux)
- `aarch64-darwin`

## Usage in NixOS / Home Manager

```nix
{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    omp.url = "github:gosha20777/omp-bin-flake";
  };

  # In home.packages:
  # home.packages = [ inputs.omp.packages.${pkgs.stdenv.hostPlatform.system}.default ];
}
```

## Update

```bash
nix flake update omp
```
