package com.example.servingwebcontent;


import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;

import com.example.servingwebcontent.ResultInterface;

public class Result extends UnicastRemoteObject implements ResultInterface {
    private String titulo, url, parag;

    public Result(String titulo, String url, String parag) throws RemoteException {
        this.titulo = titulo;
        this.url = url;
        this.parag = parag;
    }

    public String getTitulo() {
        return titulo;
    }

    public String getUrl() {
        return url;
    }

    public String getParag() {
        return parag;
    }
}