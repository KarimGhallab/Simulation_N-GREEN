# Install script for directory: /home/karim/Documents/Stage/depot_git/openjpeg-2.0.1/src/lib/openjp2

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/usr/local")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Headers")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/openjpeg-2.0" TYPE FILE FILES "/home/karim/Documents/Stage/depot_git/openjpeg-2.0.1/src/lib/openjp2/opj_config.h")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Libraries")
  foreach(file
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libopenjp2.so.2.0.1"
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libopenjp2.so.7"
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libopenjp2.so"
      )
    if(EXISTS "${file}" AND
       NOT IS_SYMLINK "${file}")
      file(RPATH_CHECK
           FILE "${file}"
           RPATH "")
    endif()
  endforeach()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE SHARED_LIBRARY FILES
    "/home/karim/Documents/Stage/depot_git/openjpeg-2.0.1/bin/libopenjp2.so.2.0.1"
    "/home/karim/Documents/Stage/depot_git/openjpeg-2.0.1/bin/libopenjp2.so.7"
    "/home/karim/Documents/Stage/depot_git/openjpeg-2.0.1/bin/libopenjp2.so"
    )
  foreach(file
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libopenjp2.so.2.0.1"
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libopenjp2.so.7"
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libopenjp2.so"
      )
    if(EXISTS "${file}" AND
       NOT IS_SYMLINK "${file}")
      if(CMAKE_INSTALL_DO_STRIP)
        execute_process(COMMAND "/usr/bin/strip" "${file}")
      endif()
    endif()
  endforeach()
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Headers")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/openjpeg-2.0" TYPE FILE FILES
    "/home/karim/Documents/Stage/depot_git/openjpeg-2.0.1/src/lib/openjp2/openjpeg.h"
    "/home/karim/Documents/Stage/depot_git/openjpeg-2.0.1/src/lib/openjp2/opj_stdint.h"
    )
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/man/man3" TYPE FILE FILES "/home/karim/Documents/Stage/depot_git/openjpeg-2.0.1/doc/man/man3/libopenjp2.3")
endif()

