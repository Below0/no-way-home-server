package com.haraorum.nowayhomeserver.controller;

import com.haraorum.nowayhomeserver.dto.Apartment;
import com.haraorum.nowayhomeserver.service.MyHomePriceService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping(value = "/price")
public class MyHomePriceController {

    private final MyHomePriceService myHomePriceService;

    @Autowired
    public MyHomePriceController(MyHomePriceService myHomePriceService) {
        this.myHomePriceService = myHomePriceService;
    }

    @GetMapping
    public List<Apartment> get(@RequestParam double lat, @RequestParam double lon, @RequestParam int radius) {
        return myHomePriceService.getPriceOfAptsWithGps(lat, lon, radius);
    }
}
