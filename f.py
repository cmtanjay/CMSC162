import var
import g

if __name__ == "__main__": 
    var.initialize()
    print(f"before: {var.x}") # print the initial value 
    g.a()
    print(f"after: {var.x}")