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
@RequestMapping(value = "/")
public class MainController {

    @GetMapping
    public String get() {
        return "Hello World! - No Way Home Server";
    }
}
