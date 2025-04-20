from custom_event_loop import MyEventLoop
import time


def main():
    loop = MyEventLoop()

    def foo():
        print("Foo")
        
    loop.call_soon(foo)

    def bar():
        print("Bar")


    loop.call_at(time.time() + 5, bar)

    loop.run_forever()


if __name__ == '__main__':
    main()