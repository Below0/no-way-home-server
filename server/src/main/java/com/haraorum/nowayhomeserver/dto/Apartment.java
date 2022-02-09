package com.haraorum.nowayhomeserver.dto;

import lombok.Data;

import java.util.Date;

@Data
public class Apartment {
    private String name;
    private String addr;
    private double lat;
    private double lon;
    private Integer avg_price;
    private Date updated_date;
}
