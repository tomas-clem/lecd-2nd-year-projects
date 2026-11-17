package com.example.servingwebcontent;

import java.rmi.Remote;
import java.rmi.RemoteException;

public interface ResultInterface extends Remote{

    public String getTitulo() throws RemoteException;
    public String getUrl() throws RemoteException;
    public String getParag() throws RemoteException;

}
