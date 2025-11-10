import hex

def main():
    grid = hex.Grid(5)
    for h in grid.Hexes:
        print(h)

if __name__ == "__main__":
    main()