package com.haraorum.nowayhomeserver.service;

import com.haraorum.nowayhomeserver.dao.ApartmentMapper;
import com.haraorum.nowayhomeserver.dto.Apartment;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class MyHomePriceService {

    private final ApartmentMapper apartmentMapper;

    @Autowired
    public MyHomePriceService(ApartmentMapper apartmentMapper) {
        this.apartmentMapper = apartmentMapper;
    }

    public List<Apartment> getPriceOfAptsWithGps(double lat, double lon, int radius) {
        String target = String.format("POINT(%f %f)", lon ,lat);
        System.out.println(target);
        return apartmentMapper.findApartmentsByGps(target, radius);
    }
}
