import argparse
from pynput.keyboard import Key, Controller
import time
import mss

debug = False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--count", type=int, default=999,
                        help="amount of cars to snipe")
    parser.add_argument("-x", type=int, default=1920,
                        help="width of the monitor Forza is on")
    parser.add_argument("-y", type=int, default=1080,
                        help="height of the monitor Forza is on")
    parser.add_argument("-w", "--wait", type=int, default=10,
                        help="time to wait before starting the script")
    parser.add_argument("-d", "--delay", type=int, default=0,
                        help="time to wait after sniping a car")
    parser.add_argument("--debug", action="store_true",
                        help="print debug messages")
    args = parser.parse_args()
    time.sleep(args.wait)
    if args.debug:
        global debug
        debug = True
    sniper_script(args.count, args.x, args.y, args.delay)


def debug_print(msg: str):
    global debug
    if debug:
        print(msg)


def getpixelcolor(x, y):
    with mss.mss() as sct:
        pic = sct.grab({'mon': 1, 'top': y, 'left': x, 'width': 1, 'height': 1})
        return pic.pixel(0, 0)


def sniper_script(collect_target: int, monitor_x: int, monitor_y: int, delay: int):

    def enter_ah():
        debug_print("Entering search")
        while getpixelcolor(ah_search_x, ah_search_y) != (255, 0, 134):
            debug_print("waiting for main auction window")
        while getpixelcolor(ah_search_x, ah_search_y) == (255, 0, 134):
            keyboard.press(Key.enter)  # Enters auction house menu
            keyboard.release(Key.enter)
            debug_print("Entering Auction House")
        while getpixelcolor(search_loading_x, search_loading_y) != (247, 247, 247):
            debug_print("p3")
            debug_print("Waiting for search")
        while getpixelcolor(s_confirm_x, s_confirm_y) != (255, 0, 134):
            debug_print("p4")
            pass
        keyboard.press(Key.enter)  # Searches the auction house
        keyboard.release(Key.enter)
        return check_for_auction()

    def check_for_auction():  # Checks the auction house for an available auction
        while getpixelcolor(rear_window_x, rear_window_y) != (255, 222, 57):  # checks if in auction list
            debug_print("waiting for auction list")
        if getpixelcolor(car_x, car_y) == (52, 23, 53):  # checks if a car is listed
            if getpixelcolor(px_x, px_y) == (247, 247, 247):
                while getpixelcolor(dj_x, dj_y) == (247, 247, 247):
                    debug_print("waiting for bidding menu")
            return attempt_buyout()
        else:  # If no available car is listed
            return_to_start()
            return False

    def attempt_buyout():  # Attempts to buyout the car
        keyboard.press(key_y)  # Auction house options
        keyboard.release(key_y)
        debug_print("Bringing up shortcut menu to purchase the car")
        time.sleep(.25)
        x, y = 0, 0
        while x == 0:
            if getpixelcolor(auction_options_x, auction_options_y) == (52, 23, 53):
                debug_print("BuyoutOption2")
                x, y = buyout_option_2x, buyout_option_2y
            elif getpixelcolor(auction_options_1x, auction_options_1y) == (52, 23, 53):
                debug_print("BuyoutOption1")
                x, y = buyout_option_x, buyout_option_y
        while getpixelcolor(x, y) != (255, 0, 134):
            keyboard.press(Key.down)  # Move to Buy-out
            keyboard.release(Key.down)
            debug_print("Moved to Buy-Out Button")
            time.sleep(.05)
        keyboard.press(Key.enter)  # Selects Buy-out
        keyboard.release(Key.enter)
        debug_print("clicked buyout")
        time.sleep(0.5)
        if getpixelcolor(budget_x, budget_y) == (255, 0, 134):
            keyboard.press(Key.enter)  # Buys the car
            keyboard.release(Key.enter)
            debug_print("Car Purchased")
        return buyout_outcome()

    def buyout_outcome():
        time.sleep(.5)
        while getpixelcolor(buyout_outcome_x, buyout_outcome_y) != (52, 23, 53):
            debug_print("Waiting for buyout outcome loading popup")
        while getpixelcolor(buyout_outcome_x, buyout_outcome_y) == (52, 23, 53):
            debug_print("Waiting for buyout outcome")
        while getpixelcolor(buyout_outcome_check_x, buyout_outcome_check_y) != (52, 23, 53):
            debug_print("Waiting for buyout outcome (2nd mysterious check)")
        if getpixelcolor(buyout_x, buyout_y) == (52, 23, 53):
            buyout_successful()
            return True
        else:
            buyout_failed()

    def buyout_successful():
        debug_print("Buyout Successful")
        keyboard.press(Key.enter)  # Backs out of the successful buy-out screen
        keyboard.release(Key.enter)
        while (255, 0, 134) not in (getpixelcolor(collect_car_x, collect_car_y),
                                    getpixelcolor(collect_car_1x, collect_car_1y),
                                    getpixelcolor(collect_car_2x, collect_car_2y)):
            debug_print("trying to collect car")
            time.sleep(.01)
        debug_print("Collect car is selected")
        time.sleep(.1)
        keyboard.press(Key.enter)  # Collects the car
        keyboard.release(Key.enter)
        time.sleep(.5)
        while getpixelcolor(collect_car_2x, collect_car_2y) == (255, 0, 134):
            keyboard.press(Key.enter)  # Collects the car
            keyboard.release(Key.enter)
            debug_print("Attempting to collect the car")
        while getpixelcolor(car_collected_x, car_collected_y) != (52, 23, 53):
            debug_print("Waiting for car to be collected")
        debug_print("Car has been collected")
        time.sleep(.1)
        keyboard.press(Key.enter)  # Collects the car
        keyboard.release(Key.enter)
        time.sleep(.7)
        keyboard.press(Key.esc)  # Backs out of the auction house shortcut menu
        keyboard.release(Key.esc)
        return_to_start()

    def buyout_failed():
        debug_print("Buyout Failed")
        while getpixelcolor(buyout_failed_x, buyout_failed_y) != (52, 23, 53):
            pass
        keyboard.press(Key.enter)  # Backs out of the successful buy-out screen
        keyboard.release(Key.enter)
        time.sleep(.7)
        time.sleep(.7)
        keyboard.press(Key.esc)  # Backs out of the auction house shortcut menu
        keyboard.release(Key.esc)
        return_to_start()

    def return_to_start():  # Returns from the auction house to the start
        while getpixelcolor(rear_window_x, rear_window_y) != (255, 222, 57):
            debug_print("Checking if there are any cars up for auction")
        keyboard.press(Key.esc)  # Returns to start location, before entering the search for the desired car
        keyboard.release(Key.esc)

    key_y = "y"

    ah_search_x = int(0.171875 * monitor_x)
    ah_search_y = int(0.2305555556 * monitor_y)
    s_confirm_x = int(0.3171875 * monitor_x)
    s_confirm_y = int(0.677777778 * monitor_y)
    rear_window_x = int(0.2140625 * monitor_x)
    rear_window_y = int(0.159259259 * monitor_y)
    car_x = int(0.515625 * monitor_x)
    car_y = int(0.213888889 * monitor_y)
    px_x = int(0.4546875 * monitor_x)
    px_y = int(0.216666667 * monitor_y)
    dj_x = int(0.4546875 * monitor_x)
    dj_y = int(0.216666667 * monitor_y)
    buyout_option_x = int(0.329166667 * monitor_x)
    buyout_option_y = int(0.492592593 * monitor_y)
    budget_x = int(0.3265625 * monitor_x)
    budget_y = int(0.52962963 * monitor_y)
    buyout_outcome_x = int(0.33489583333 * monitor_x)
    buyout_outcome_y = int(0.40925925925 * monitor_y)
    buyout_x = int(0.3328125 * monitor_x)
    buyout_y = int(0.42592592592 * monitor_y)
    collect_car_1x = int(0.32291666666 * monitor_x)
    collect_car_1y = int(0.46481481481 * monitor_y)
    collect_car_x = int(0.328645833 * monitor_x)
    collect_car_y = int(0.490740741 * monitor_y)
    car_collected_x = int(0.3296875 * monitor_x)
    car_collected_y = int(0.47685185185 * monitor_y)
    buyout_failed_x = int(0.33020833333 * monitor_x)
    buyout_failed_y = int(0.49259259259 * monitor_y)
    collect_car_2x = int(0.31818181818 * monitor_x)
    collect_car_2y = int(0.46666666666 * monitor_y)
    buyout_option_2x = int(0.32916666666 * monitor_x)
    buyout_option_2y = int(0.47592592592 * monitor_y)
    auction_options_x = int(0.32864583333 * monitor_x)
    auction_options_y = int(0.3537037037 * monitor_y)
    auction_options_1x = int(0.33020833333 * monitor_x)
    auction_options_1y = int(0.41944444444 * monitor_y)
    search_loading_x = int(0.4703125 * monitor_x)
    search_loading_y = int(0.52962962963 * monitor_y)
    buyout_outcome_check_x = int(0.33020833333 * monitor_x)
    buyout_outcome_check_y = int(0.47685185185 * monitor_y)

    keyboard = Controller()
    collected = 0
    before = time.time()
    while collected < collect_target:
        if enter_ah():
            collected += 1
            print(f"time spent: {round(time.time() - before)} sec")
            if collected != collect_target:
                time.sleep(delay)
            before = time.time()


if __name__ == "__main__":
    main()
