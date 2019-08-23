from User import User

def main():

    stav=User("stav","Cohen")
   # stav.add_bench_press_weights([20,40,90,10])
    #stav.add_bench_press_dates(("12/2","14/2","22/2","24/2"))
    stav.read_csv()
    stav.plot_exercise()




if __name__ == '__main__':
    main()