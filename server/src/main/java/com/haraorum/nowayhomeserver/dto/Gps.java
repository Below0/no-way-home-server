package com.haraorum.nowayhomeserver.dto;

import lombok.AllArgsConstructor;
import lombok.Data;

import java.util.Date;

@Data
@AllArgsConstructor
public class Gps {
    private double lat;
    private double lon;
    private int radius;
}
