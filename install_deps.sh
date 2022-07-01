#!/bin/bash

# Run pacman to update
pacman -Syyu --noconfirm

# Install basic packages
pacman -S --noconfirm base-devel git neofetch jq

# Install rust toolchain, cargo and other required packages
curl https://sh.rustup.rs -sSf | sh -s -- -y

# Update $PATH
export PATH="$HOME/.cargo/bin:$PATH"

# Build project
cargo build --release
