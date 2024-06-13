$(document).ready(function() {
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $('#user-search').on('keyup', function() {
        let query = $(this).val();
        if (query.length > 0) {
            $.ajax({
                url: '{% url "search_users" %}',
                data: {
                    'q': query
                },
                dataType: 'json',
                success: function(data) {
                    console.log(data); // добавьте эту строку
                    $('#search-results').empty();
                    if (data.results.length > 0) {
                        let results = data.results;
                        results.forEach(function(result) {
                            console.log(result); // добавьте эту строк
                            if (result.type == 'channel') {
                                // Формируем HTML-код для отображения информации о канале
                                $('#search-results').append(`
                                    <div class="channel-item-profile" data-id="${result.id}">
                                        <img src="${result.avatar_c}" class="avatar" alt="${result.name_c}">
                                        <span class="username">${result.name_c}</span>
                                    </div>
                                `);
                            } else {
                                // Формируем HTML-код для отображения информации о пользователе
                                $('#search-results').append(`
                                    <div class="user-item-profile" data-id="${result.id}">
                                        <img src="${result.avatar}" class="avatar" alt="${result.username}">
                                        <span class="username">${result.username}</span>
                                    </div>
                                `);
                            }
                        });
                    } else {
                        $('#search-results').append('<div>No results found</div>');
                    }
                }
            });
        } else {
            $('#search-results').empty();
        }
    });
    $(document).on('click', '.channel-item-profile', function() {
        let channelId = $(this).data('id');
        window.location.href = `/channel_detail/${channelId}/`;
    });
    $(document).on('click', '.user-item-profile', function() {
        let userId = $(this).data('id');
        window.location.href = `/view_profile/${userId}/`;
    });
});
  // Инициализируем текстовое поле emojionearea для поля `content`
$('#id_content').emojioneArea({
    pickerPosition: 'bottom',
    tonesStyle: 'bullet'
});