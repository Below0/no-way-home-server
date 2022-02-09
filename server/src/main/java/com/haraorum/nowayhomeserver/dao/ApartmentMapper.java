package com.haraorum.nowayhomeserver.dao;

import com.haraorum.nowayhomeserver.dto.Apartment;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Result;
import org.apache.ibatis.annotations.Results;
import org.apache.ibatis.annotations.Select;

import java.util.List;

@Mapper
public interface ApartmentMapper {

    @Results({
            @Result(property = "name", column = "apt_name"),
            @Result(property = "addr", column = "address"),
            @Result(property = "lon", column = "lon"),
            @Result(property = "lat", column = "lat"),
            @Result(property = "avg_price", column = "avg_price"),
            @Result(property = "updated_date", column = "updated_date")
    })
    @Select("SELECT apt_name, address, ST_Y(lat_lon) AS lon, ST_X(lat_lon) AS lat, avg_price, updated_date " +
            "FROM apt_info " +
            "WHERE ST_Distance_Sphere(lat_lon, ST_GeomFromText(#{point})) <= #{radius}")
    public List<Apartment> findApartmentsByGps(String point, int radius);

    @Results({
            @Result(property = "name", column = "apt_name"),
            @Result(property = "addr", column = "address"),
            @Result(property = "lon", column = "lon"),
            @Result(property = "lat", column = "lat"),
            @Result(property = "avg_price", column = "avg_price"),
            @Result(property = "updated_date", column = "updated_date")
    })
    @Select("SELECT apt_name, address, ST_Y(lat_lon) AS lon, ST_X(lat_lon) AS lat, avg_price, updated_date FROM apt_info")
    public List<Apartment> findAllApartments();
}
