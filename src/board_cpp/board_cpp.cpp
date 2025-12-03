#include <stdio.h>
#include "pico/stdlib.h"
#include "pico/cyw43_arch.h"
#include "FreeRTOS.h"
#include "task.h"
#include "lwip/sockets.h"
#include <cstring>
#include <cstdio>

const uint8_t blue_led = 14;
const uint8_t  red_led = 15;


int main()
{
    stdio_init_all();

    gpio_init(blue_led);
    gpio_init( red_led);

    gpio_set_dir(blue_led, GPIO_OUT);
    gpio_set_dir( red_led, GPIO_OUT);


    // Initialise the Wi-Fi chip
    if (cyw43_arch_init()) {
        printf("Wi-Fi init failed\n");
        return -1;
    }

    // Enable wifi station
    cyw43_arch_enable_sta_mode();

    printf("Connecting to Wi-Fi...\n");
    if (cyw43_arch_wifi_connect_timeout_ms("TP-Link_4FEC", "HelloWorld", CYW43_AUTH_WPA2_AES_PSK, 30000)) {
        printf("failed to connect.\n");
        return 1;
    } else {
        printf("Connected.\n");
        // Read the ip address in a human readable way
        uint8_t *ip_address = (uint8_t*)&(cyw43_state.netif[0].ip_addr.addr);
        printf("IP address %d.%d.%d.%d\n", ip_address[0], ip_address[1], ip_address[2], ip_address[3]);
    }

    while (true) {
        printf("Hello, world!\n");
        cyw43_arch_gpio_put(CYW43_WL_GPIO_LED_PIN, 1);
        gpio_put( red_led, false);
        gpio_put(blue_led, true);
        sleep_ms(1000);
        cyw43_arch_gpio_put(CYW43_WL_GPIO_LED_PIN, 0);
        gpio_put(blue_led, false);
        gpio_put( red_led, true);
        sleep_ms(1000);
    }
}
